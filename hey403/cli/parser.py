import argparse


def create_base_parser():
    return argparse.ArgumentParser(
        description="Hey 404 DNS Analyzer",
        add_help=False)


def add_common_arguments(parser):

    parser.add_argument(
        "--set",
        action="store_true",
        help="Set Best DNS on system (e.g: Google, Cloudflare)",
    )

    parser.add_argument(
        "--unset",
        action="store_true",
        help="Unset Current DNS on system",
    )

    parser.add_argument(
        "-c",
        "--current-dns",
        action="store_true",
        help="Get Current DNS on system",
    )

    return parser


def build_parser():
    parser = create_base_parser()
    parser = add_common_arguments(parser)
    return parser
