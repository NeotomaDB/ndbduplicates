from rich.console import Console
from rich.table import Table

def print_fk_tables(tables):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Related Tables", style="dim")
    for i in tables:
        table.add_row(i[0])
    console.print(table)