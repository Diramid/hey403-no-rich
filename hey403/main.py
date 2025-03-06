import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console
from rich.progress import Progress

from hey403.cli.parser import build_parser
from hey403.network.dns_servers import DNS_SERVERS
from hey403.services.dns_resolver import (
    set_dns,
    test_dns,
    ensure_protocol,
    get_current_dns,
    unset_dns,
)
from hey403.utils.network_utils import check_internet_connection
from hey403.utils.table import create_table


def main():
    try:
        check_internet_connection()

        parser = build_parser()
        args = parser.parse_args()

        console = Console()
        table = create_table()
        dns_success_list = []

        if args.current_dns:
            current_dns = get_current_dns()
            dns = [dns for dns in DNS_SERVERS if dns["preferred"] == current_dns]
            if dns:
                console.print(
                    "[yellow]Current DNS[/yellow]: ",
                    f"[cyan]{dns[0]['name']}[/cyan] which {dns[0]['preferred']} ip",
                )
            else:
                console.print(
                    "[yellow]Current DNS[/yellow]: ",
                    f"[cyan]Custom DNS[/cyan] - {current_dns} (not in DNS_SERVERS)",
                )
            sys.exit(0)

        elif args.unset:
            unset_dns()
            console.print("[green]DNS unset Successfully[/green]")
            sys.exit(0)

        if not args.url:
            console.print(
                "[red]Error: URL is required when not using --current-dns or --unset[/red]"
            )
            sys.exit(1)

        args.url = ensure_protocol(args.url)

        with Progress(console=console) as progress:
            task = progress.add_task(
                "[cyan]Testing DNS servers...", total=len(DNS_SERVERS)
            )
            with ThreadPoolExecutor(max_workers=min(32, len(DNS_SERVERS))) as executor:
                futures = {
                    executor.submit(test_dns, dns, args.url): dns for dns in DNS_SERVERS
                }
                for future in as_completed(futures):
                    try:
                        (
                            dns_name,
                            preferred_dns,
                            alternative_dns,
                            status_message,
                            response_time_display,
                        ) = future.result()
                        table.add_row(
                            dns_name,
                            preferred_dns,
                            alternative_dns,
                            status_message,
                            response_time_display,
                        )
                        if args.set and status_message == "[green]Success[/green]":
                            dns_success_list.append(
                                [
                                    dns_name,
                                    preferred_dns,
                                    alternative_dns,
                                    response_time_display,
                                ]
                            )
                    except Exception as e:
                        console.print(f"[red]Error testing DNS: {e}[/red]")
                    progress.update(task, advance=1)

        if args.set and dns_success_list:
            min_entry = min(dns_success_list, key=lambda x: float(x[-1].strip(" ms")))
            set_dns(min_entry[1], min_entry[2])
            console.print(f'"{min_entry[0]}" DNS set Successfully')

        console.print(table)

    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
