import time
from dns import resolver
from src.network.ban_ips import BAN_IPS


def test_dns_with_custom_ip(url: str, dns_ip: str) -> (str, float):
    """
    Tests the DNS configuration by sending a request to a specific URL using a custom DNS IP.
    Returns the number of records found and the response time.
    """
    hostname = url.split("//")[-1].split("/")[0]
    start_time = time.perf_counter()

    try:
        custom_resolver = resolver.Resolver()
        custom_resolver.nameservers = [dns_ip]
        custom_resolver.timeout = 5
        custom_resolver.lifetime = 5

        result = custom_resolver.resolve(hostname, 'A', raise_on_no_answer=False)
        response_time = time.perf_counter() - start_time
        ip = result.rrset._rdata_repr()
        ip = ip[ip.find("<") + 1: ip.find(">")]

        if ip in BAN_IPS:
            return 451, 0
        return 200, response_time

    except (
            resolver.NoAnswer,
            resolver.NXDOMAIN,
            resolver.LifetimeTimeout,
            resolver.NoNameservers,
    ):
        return 500, 0
