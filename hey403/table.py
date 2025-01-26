from rich.table import Table


def create_table() -> Table:
    """Creates and returns a Rich Table for displaying results."""
    table = Table(title="DNS Response Time Test", title_style="bold magenta")
    table.add_column("DNS Name", style="cyan", justify="left")
    table.add_column("Preferred DNS", style="green", justify="left")
    table.add_column("Alternative DNS", style="green", justify="left")
    table.add_column("Request Status", style="yellow", justify="center")
    table.add_column("Response Time (s)", style="magenta", justify="right")
    return table
