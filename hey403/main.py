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
        parser = build_parser()
        args = parser.parse_args()

        check_internet_connection()

        if args.current_dns:
            current_dns = get_current_dns()
            dns = [dns for dns in DNS_SERVERS if dns["preferred"] == current_dns]
            if dns:
                print(dns[0]['preferred'])
            else:
                print(current_dns)
            sys.exit(0)

        if args.unset:
            unset_dns()
            sys.exit(0)

        if not args.url:
            print("Error: URL is required when not using --current-dns or --unset")
            sys.exit(1)

        args.url = ensure_protocol(args.url)

        results = []
        dns_success_list = []

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
                    # Simplify status_message for output
                    status = "Success" if "Success" in status_message else "Failed"
                    result = [
                        dns_name,
                        preferred_dns,
                        alternative_dns,
                        status,
                        response_time_display,
                    ]
                    results.append(result)
                    if args.set and status == "Success":
                        dns_success_list.append(result)
                except Exception as e:
                    print(f"Error testing DNS: {e}")

        if args.set and dns_success_list:
            fastest = min(dns_success_list, key=lambda x: float(x[-1].strip(" ms")))
            set_dns(fastest[1], fastest[2])
            print(f'"{fastest[0]}" DNS set successfully')


    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()