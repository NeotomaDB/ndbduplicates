from rich.console import Console
from rich.table import Table

def print_fk_tables(tables):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Related Schema", style="dim")
    table.add_column("Related Table", style="dim")
    table.add_column("Related Column", style="dim")
    for i in tables:
        table.add_row(i['constraint_schema'], i['table_name'], i['column_name'])
    console.print(table)