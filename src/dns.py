import time
import dns.resolver


def test_dns_with_custom_ip(url: str, dns_ip: str) -> (str, float):
    """
    Tests the DNS configuration by sending a request to a specific URL using a custom DNS IP.
    Returns the number of records found and the response time.
    """
    hostname = url.split("//")[-1].split("/")[0]
    start_time = time.perf_counter()

    try:
        custom_resolver = dns.resolver.Resolver()
        custom_resolver.nameservers = [dns_ip]
        custom_resolver.timeout = 10
        custom_resolver.lifetime = 10

        result = custom_resolver.resolve(hostname, 'A', raise_on_no_answer=False)
        response_time = time.perf_counter() - start_time
        return len(result), response_time

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout) as e:
        print(f"Error resolving {hostname} with DNS {dns_ip}: {e}")
        return "Failed", float('inf')
