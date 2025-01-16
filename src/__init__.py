import argparse
from rich.console import Console
from rich.progress import Progress
from src.dns import test_dns_with_custom_ip
from src.table import create_table

# Define DNS servers with their names and preferred/alternative DNS
DNS_SERVERS = [
    {"name": "Google Public DNS", "preferred": "8.8.8.8", "alternative": "8.8.4.4"},
    {"name": "Electro", "preferred": "78.157.42.100", "alternative": "78.157.42.101"},
    {"name": "Cloudflare", "preferred": "1.1.1.1", "alternative": "1.0.0.1"},
    {"name": "OpenDNS", "preferred": "208.67.222.222", "alternative": "208.67.220.220"},
    {"name": "Quad9", "preferred": "9.9.9.9", "alternative": "149.112.112.112"},
    {"name": "Comodo Secure DNS", "preferred": "8.26.56.26", "alternative": "8.20.247.20"},
    {"name": "DNS.Watch", "preferred": "84.200.69.80", "alternative": "84.200.70.40"},
    {"name": "Verisign Public DNS", "preferred": "64.6.64.6", "alternative": "64.6.65.6"},
    {"name": "Yandex DNS", "preferred": "77.88.8.8", "alternative": "77.88.8.1"},
    {"name": "CleanBrowsing", "preferred": "185.228.168.9", "alternative": "185.228.169.9"},
    {"name": "OpenNIC", "preferred": "185.121.177.177", "alternative": "169.239.202.202"},
    {"name": "FreeDNS", "preferred": "37.235.1.174", "alternative": "37.235.1.177"},
    {"name": "Neustar UltraDNS", "preferred": "156.154.70.1", "alternative": "156.154.71.1"},
    {"name": "SafeDNS", "preferred": " 195.46.39.39", "alternative": "195.46.39.40"},
    {"name": "AdGuard DNS", "preferred": "94.140.14.14", "alternative": "94.140.15.15"},
    {"name": "Hurricane Electric", "preferred": "74.82.42.42", "alternative": None},
]

def main():
    parser = argparse.ArgumentParser(description="Test DNS resolution for a given URL using predefined DNS servers.")
    parser.add_argument("url", type=str, help="The URL to test.")
    args = parser.parse_args()

    console = Console()
    table = create_table()

    with Progress() as progress:
        task = progress.add_task("[cyan]Testing DNS servers...", total=len(DNS_SERVERS))

        for dns in DNS_SERVERS:
            dns_name = dns["name"]
            preferred_dns = dns["preferred"]
            alternative_dns = dns["alternative"]

            status, response_time = test_dns_with_custom_ip(args.url, preferred_dns)

            status_message = "[green]Success[/green]" if status != "Failed" else "[red]Failed[/red]"
            response_time_display = f"{response_time:.4f}" if response_time < float('inf') else "N/A"

            table.add_row(dns_name, preferred_dns, alternative_dns, status_message, response_time_display)
            progress.update(task, advance=1)

    console.print(table)

if __name__ == "__main__":
    main()