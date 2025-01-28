import ctypes
import subprocess


def get_activate_interface():
    try:
        result = subprocess.check_output(
            ["netsh", "interface", "show", "interface"], text=True
        ).splitlines()

        active_interfaces = [
            line.split()[-1] for line in result if "Connected" in line
        ]
        return active_interfaces

    except Exception as e:
        print(f"Failed to get active interfaces: {e}")
        return []


def get_active_connections():
    try:
        result = subprocess.check_output(
            ["nmcli", "-t", "-f", "NAME", "connection", "show", "--active"], text=True
        ).splitlines()
        active_connections = [
            connection for connection in result
        ]
        return active_connections
    except FileNotFoundError as e:
        print(f"Failed to get active connections, dependency {e.filename} is not installed")
        return []
    except Exception as e:
        print(f"Failed to get active connections: {e}")
        return []


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
