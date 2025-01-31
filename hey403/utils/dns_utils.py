import ctypes
import logging
import os
import subprocess
import sys

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get_status_code_from_request(ip: str):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    try:
        response = requests.get(
            url=f"https://{ip}",
            timeout=10,
            verify=False
        )
        return response.status_code

    except requests.exceptions.RequestException as e:
        return None


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


def configure_linux_dns(preferred_dns: str, alternative_dns: str | None) -> None:
    if os.geteuid() != 0:
        logging.error("Please run with sudo!")
        sys.exit(1)

    active_connections = get_active_connections()
    if not active_connections:
        logging.error("No active network connections found.")
        sys.exit(1)

    active_connection = active_connections[0]
    dns_servers = f"{preferred_dns} {alternative_dns}" if alternative_dns else preferred_dns

    if not configure_dns(connection=active_connection, dns_servers=dns_servers):
        logging.error(f"Failed to configure DNS({dns_servers}) on connection {active_connection}")
        sys.exit(1)

    logging.info("DNS successfully set for connection: %s!", active_connection)


def configure_windows_dns(preferred_dns: str, alternative_dns: str | None) -> None:
    if not is_admin():
        logging.error("Please run as Administrator!")
        logging.warning("You can run cmd or power shell as Administrator!")
        sys.exit(1)

    interface = get_activate_interface()
    if not interface:
        logging.error("No active interface found!")
        sys.exit(1)

    interface_name = interface[0]
    try:
        subprocess.run(
            f'netsh interface ip set dns "{interface_name}" static {preferred_dns} primary',
            shell=True,
            check=True,
        )

        if alternative_dns:
            subprocess.run(
                f'netsh interface ip add dns "{interface_name}" {alternative_dns} index=2',
                shell=True,
                check=True,
            )

        logging.info("DNS successfully set!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting DNS: {e}")
        sys.exit(1)


def configure_mac_dns(preferred_dns: str, alternative_dns: str | None) -> None:
    try:
        connection_type = None
        for interface in ["Wi-Fi", "Ethernet"]:
            try:
                subprocess.run(
                    f"networksetup -getdnsservers {interface}",
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                )
                connection_type = interface
                break
            except subprocess.CalledProcessError:
                continue

        if not connection_type:
            logging.error("No active network interfaces (Wi-Fi or Ethernet) found!")
            sys.exit(1)

        base_command = f"networksetup -setdnsservers {connection_type}"
        dns_servers = f"{preferred_dns} {alternative_dns}" if alternative_dns else preferred_dns

        subprocess.run(
            f"{base_command} {dns_servers}",
            shell=True,
            check=True,
        )

        logging.info("DNS successfully set for %s!", connection_type)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while setting DNS: {e}")
        sys.exit(1)


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()
