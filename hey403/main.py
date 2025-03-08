import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def main():
    try:
        check_internet_connection()

        parser = build_parser()
        args = parser.parse_args()

        dns_success_list = []

        if args.current_dns:
            current_dns = get_current_dns()
            dns = [dns for dns in DNS_SERVERS if dns["preferred"] == current_dns]
            if dns:
                print(f"{dns[0]['name']} ({dns[0]['preferred']} IP)")
            else:
                print(f"Custom DNS - {current_dns} (not in DNS_SERVERS)")
            sys.exit(0)

        elif args.unset:
            unset_dns()
            print("DNS unset Successfully")
            sys.exit(0)

        if not args.url:
            print("Error: URL is required when not using --current-dns or --unset")
            sys.exit(1)

        args.url = ensure_protocol(args.url)

        print("Testing DNS servers...")
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
                    print(
                        f"{dns_name}: {preferred_dns} | {alternative_dns} | {status_message} | {response_time_display}"
                    )
                    if args.set and "Success" in status_message:
                        dns_success_list.append(
                            [
                                dns_name,
                                preferred_dns,
                                alternative_dns,
                                response_time_display,
                            ]
                        )
                except Exception as e:
                    print(f"Error testing DNS: {e}")

        if args.set and dns_success_list:
            min_entry = min(dns_success_list, key=lambda x: float(x[-1].strip(" ms")))
            set_dns(min_entry[1], min_entry[2])
            print(f'"{min_entry[0]}" DNS set Successfully')

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
