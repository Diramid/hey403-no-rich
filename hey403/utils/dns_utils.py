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


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
