import argparse

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(force_terminal=True)

    def format_help(self):
        help_text = Text()

        # Title
        help_text.append("HEY 403 DNS ANALYZER", style="bold magenta")
        help_text.append(" 🌐🕵️‍♂️\n\n", style="bold cyan")

        # Usage
        help_text.append("Usage:", style="bold yellow")
        help_text.append("\n  ")
        help_text.append("hey403", style="bold cyan")
        help_text.append(" ", style="reset")
        help_text.append("[URL]", style="bold green")
        help_text.append(" ", style="reset")
        help_text.append("[OPTIONS]\n\n", style="bold cyan")

        # Positional Arguments
        help_text.append("Positional Arguments:", style="bold yellow")
        help_text.append("\n  ")
        help_text.append("URL", style="bold green")
        help_text.append("         Target URL/domain to test (e.g. ")
        help_text.append("example.com", style="bold green")
        help_text.append(")\n\n")

        # Optional Arguments
        help_text.append("Optional Arguments:", style="bold yellow")
        help_text.append("\n  ")
        help_text.append("-h, --help", style="bold cyan")
        help_text.append("     Show this help message 🆘\n  ")
        help_text.append("--url", style="bold cyan")
        help_text.append("          Alternate URL specification\n  ")
        help_text.append("--set", style="bold cyan")
        help_text.append("          Set Best DNS on system (e.g: Google, Cloudflare)\n  ")
        help_text.append("-c, --current-dns", style="bold cyan")
        help_text.append("  Display the current DNS settings of the system 📡\n  ")
        help_text.append("--unset", style="bold cyan")
        help_text.append("        Remove custom DNS settings and revert to default 🔄\n\n")

        # Examples
        help_text.append("Examples:", style="bold yellow")
        help_text.append("\n  ")
        help_text.append("hey403", style="bold cyan")
        help_text.append(" ")
        help_text.append("example.com \n", style="bold green")
        help_text.append("  hey403", style="bold cyan")
        help_text.append(" ")
        help_text.append("--url", style="bold cyan")
        help_text.append(" google.com 💫\n", style="bold green")
        help_text.append("  hey403", style="bold cyan")
        help_text.append(" ")
        help_text.append("google.com ", style="bold green")
        help_text.append("--set \n", style="bold green")
        help_text.append("  hey403", style="bold cyan")
        help_text.append(" ")
        help_text.append("--url", style="bold cyan")
        help_text.append(" google.com ", style="bold green")
        help_text.append("--set \n", style="bold green")
        help_text.append("  hey403", style="bold cyan")
        help_text.append(" ")
        help_text.append("-c \n", style="bold green")
        help_text.append("  hey403", style="bold cyan")
        help_text.append(" ")
        help_text.append("--unset \n", style="bold green")

        # Footer
        help_text.append("\n")
        help_text.append("Use this power responsibly! ", style="italic")
        help_text.append("⚠️", style="bold red")

        panel = Panel(
            help_text,
            title="Help Documentation",
            border_style="bright_magenta",
            padding=(1, 4),
            width=80,
        )

        with self.console.capture() as capture:
            self.console.print(panel)
        return capture.get()