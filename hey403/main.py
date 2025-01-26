from rich.console import Console
from rich.progress import Progress

from hey403.cli.parser import build_parser
from hey403.dns_resolver import test_dns_with_custom_ip
from hey403.table import create_table
from hey403.network.dns_servers import DNS_SERVERS
from concurrent.futures import ThreadPoolExecutor, as_completed


def test_dns(dns, url):
    dns_name = dns["name"]
    preferred_dns = dns["preferred"]
    alternative_dns = dns["alternative"]

    status, response_time = test_dns_with_custom_ip(url, preferred_dns)
    status_message = "[green]Success[/green]" if status == 200 else "[red]Failed[/red]"
    response_time_display = f"{response_time:.4f}" if response_time < float('inf') else "N/A"

    return (dns_name, preferred_dns, alternative_dns, status_message, response_time_display)


def main():
    parser = build_parser()
    args = parser.parse_args()

    console = Console()

    table = create_table()

    with Progress() as progress:
        task = progress.add_task("[cyan]Testing DNS servers...", total=len(DNS_SERVERS))

        with ThreadPoolExecutor(max_workers=min(32, len(DNS_SERVERS))) as executor:
            futures = {executor.submit(test_dns, dns, args.url): dns for dns in DNS_SERVERS}

            for future in as_completed(futures):
                dns_name, preferred_dns, alternative_dns, status_message, response_time_display = future.result()
                table.add_row(dns_name, preferred_dns, alternative_dns, status_message, response_time_display)
                progress.update(task, advance=1)

    console.print(table)


if __name__ == "__main__":
    main()
