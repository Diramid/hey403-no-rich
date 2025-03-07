import argparse


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format_help(self):
        help_text = []

        # Title
        help_text.append("HEY 403 DNS ANALYZER\n")
        help_text.append(" 🌐🕵️‍♂️\n\n")

        # Usage
        help_text.append("Usage:\n")
        help_text.append("  hey403 [URL] [OPTIONS]\n\n")

        # Positional Arguments
        help_text.append("Positional Arguments:\n")
        help_text.append("  URL         Target URL/domain to test (e.g. example.com)\n\n")

        # Optional Arguments
        help_text.append("Optional Arguments:\n")
        help_text.append("  -h, --help     Show this help message 🆘\n")
        help_text.append("  --url          Alternate URL specification\n")
        help_text.append("  --set          Set Best DNS on system (e.g: Google, Cloudflare)\n")
        help_text.append("  -c, --current-dns  Display the current DNS settings of the system 📡\n")
        help_text.append("  --unset        Remove custom DNS settings and revert to default 🔄\n\n")

        # Examples
        help_text.append("Examples:\n")
        help_text.append("  hey403 example.com\n")
        help_text.append("  hey403 --url google.com 💫\n")
        help_text.append("  hey403 google.com --set\n")
        help_text.append("  hey403 --url google.com --set\n")
        help_text.append("  hey403 -c\n")
        help_text.append("  hey403 --unset\n")

        # Footer
        help_text.append("\n")
        help_text.append("Use this power responsibly! ⚠️")

        return "\n".join(help_text)
