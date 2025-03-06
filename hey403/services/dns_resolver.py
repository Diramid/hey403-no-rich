import logging
import platform
import sys
import time
from urllib.parse import urlparse

from dns import resolver

from hey403.network.ban_ips import BAN_IPS
from hey403.utils.dns_utils import get_status_code_from_request, DNSManager

dns_manager = DNSManager()


def ensure_protocol(url: str) -> str:
    """
    Ensure the URL has a protocol (http:// or https://).
    If not, add https:// by default.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f"https://{url}"
    return url

def test_dns_with_custom_ip(url: str, dns_ip: str) -> (str, float):
    """
    Tests the DNS configuration by sending a request to a specific URL using a custom DNS IP.
    Returns the number of records found and the response time.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    url = ensure_protocol(url)

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if hostname is None:
        logging.error(f"Invalid URL: {url}")
        return 500, 0.0

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


def set_dns(preferred_dns: str, alternative_dns: str | None = None) -> None:
    dns_manager.configure_dns(preferred_dns, alternative_dns)


def get_current_dns() -> str:
    return dns_manager.get_current_dns()


def test_dns(dns, url):
def unset_dns() -> None:
    dns_manager.unset_dns()


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
