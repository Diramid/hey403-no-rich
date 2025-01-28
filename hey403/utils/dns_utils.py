import ctypes
import logging
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
    """
    Retrieves the names of active network connections to monitor and manage current network activity.
    This helps in understanding which networks are currently in use on the system.
    """
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


def run_command(command: [str], error_message: str) -> bool:
    """
    Executes a shell command to perform an action and logs an error if the command fails.
    """
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"{error_message}: {e}")
        return False


def configure_dns(connection: str, dns_servers: str) -> bool:
    """
    Sets custom DNS servers for a network connection and ensures the changes take effect.
    """
    commands = [
        (
            ["nmcli", "connection", "modify", connection, "ipv4.dns", dns_servers],
            f"Failed to set DNS for connection {connection}"
        ),
        (
            ["nmcli", "connection", "modify", connection, "ipv4.ignore-auto-dns", "yes"],
            f"Failed to ignore auto-DNS on connection {connection}"
        ),
        (
            ["systemctl", "restart", "NetworkManager"],
            "Failed to restart NetworkManager"
        )
    ]
    for command, error_message in commands:
        if not run_command(command, error_message):
            return False
    return True


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
