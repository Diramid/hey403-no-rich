import logging
import os
import platform
import subprocess
import sys
import time
from urllib.parse import urlparse

from dns import resolver

from hey403.network.ban_ips import BAN_IPS
from hey403.utils.dns_utils import is_admin, get_activate_interface, get_active_connections, configure_dns, \
    get_status_code_from_request


def test_dns_with_custom_ip(url: str, dns_ip: str) -> (str, float):
    """
    Tests the DNS configuration by sending a request to a specific URL using a custom DNS IP.
    Returns the number of records found and the response time.
    """
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    start_time = time.perf_counter()

    dns_failure_time = 0.0

    try:
        custom_resolver = resolver.Resolver()
        custom_resolver.nameservers = [dns_ip]
        custom_resolver.timeout = 5
        custom_resolver.lifetime = 5

        result = custom_resolver.resolve(hostname, "A", raise_on_no_answer=False)
        response_time = time.perf_counter() - start_time
        ip = result.rrset._rdata_repr()
        ip = ip[ip.find("<") + 1: ip.find(">")]

        if ip in BAN_IPS:
            return 451, dns_failure_time

        status_code = get_status_code_from_request(ip)

        if status_code == 403:
            return 403, dns_failure_time

        return 200, response_time


    except (
            resolver.NoAnswer,
            resolver.NXDOMAIN,
            resolver.LifetimeTimeout,
            resolver.NoNameservers,
    ):
        return 500, dns_failure_time


def set_dns(preferred_dns, alternative_dns=None):
    """
    Configures DNS settings for the current system based on the platform.

    Supports Linux, Windows, and macOS (Darwin) by setting the preferred and optional alternative
    DNS servers for the active network connection or interface.
    """
    system_platform = platform.system()

    if system_platform == "Linux":
        if os.geteuid() == 0:
            active_connections = get_active_connections()
            if not active_connections:
                logging.error("No active network connections found.")
                sys.exit(1)
            active_connection = active_connections[0]

            dns_servers = preferred_dns
            if alternative_dns:
                dns_servers += f" {alternative_dns}"

            result = configure_dns(connection=active_connection, dns_servers=dns_servers)
            if not result:
                logging.error(f"Failed to configure DNS({dns_servers}) on connection {active_connection}. exit code: 1")
                sys.exit(1)
            logging.info(f"DNS successfully set for connection: {active_connection}!")
            sys.exit(0)
        else:
            logging.error("Please run with sudo!")
            sys.exit(1)

    elif system_platform == "Windows":
        if not is_admin():
            logging.error("Please run as Administrator!")
            logging.warning(
                "You can run cmd (command line) or power shell as Administrator! "
            )
            sys.exit(1)

        try:
            interface = get_activate_interface()

            if not interface:
                logging.error("No active interface found!")
                sys.exit(1)

            interface_name = interface[0]
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

    elif system_platform == "Darwin":
        try:
            wifi_command = "networksetup -setdnsservers Wi-Fi"
            ethernet_command = "networksetup -setdnsservers Ethernet"

            try:
                subprocess.run(
                    f"networksetup -getdnsservers Wi-Fi",
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                )
                connection_type = "Wi-Fi"
            except subprocess.CalledProcessError:
                try:
                    subprocess.run(
                        f"networksetup -getdnsservers Ethernet",
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                    )
                    connection_type = "Ethernet"
                except subprocess.CalledProcessError:
                    logging.error(
                        "No active network interfaces (Wi-Fi or Ethernet) found!"
                    )
                    sys.exit(1)

            if connection_type == "Wi-Fi":
                logging.info("Configuring DNS for Wi-Fi...")
                subprocess.run(
                    f"{wifi_command} {preferred_dns}", shell=True, check=True
                )
                if alternative_dns:
                    subprocess.run(
                        f"{wifi_command} {preferred_dns} {alternative_dns}",
                        shell=True,
                        check=True,
                    )

            elif connection_type == "Ethernet":
                logging.info("Configuring DNS for Ethernet...")
                subprocess.run(
                    f"{ethernet_command} {preferred_dns}", shell=True, check=True
                )
                if alternative_dns:
                    subprocess.run(
                        f"{ethernet_command} {preferred_dns} {alternative_dns}",
                        shell=True,
                        check=True,
                    )

            logging.info("DNS successfully set!")

        except subprocess.CalledProcessError as e:
            logging.error(f"Error while setting DNS: {e}")
            sys.exit(1)

    else:
        logging.error(f"Unsupported platform: {system_platform}")
        sys.exit(1)


def test_dns(dns, url):
    dns_name = dns["name"]
    preferred_dns = dns["preferred"]
    alternative_dns = dns["alternative"]

    status, response_time = test_dns_with_custom_ip(url, preferred_dns)
    status_message = "[green]Success[/green]" if status == 200 else "[red]Failed[/red]"
    response_time_display = (
        f"{response_time:.4f}" if response_time < float("inf") else "N/A"
    )

    return (
        dns_name,
        preferred_dns,
        alternative_dns,
        status_message,
        response_time_display,
    )
