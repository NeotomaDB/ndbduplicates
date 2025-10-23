from rich.console import Console
from rich.table import Table

def print_row_results(rowresults, rows):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Related Schema", style="dim")
    table.add_column("Related Table", style="dim")
    table.add_column("Related Column", style="dim")
    table.add_column(f"RowID {rows[0]}", style="dim")
    table.add_column(f"RowID {rows[1]}", style="dim")
    for i in rowresults:
        table.add_row(*[str(k) for k in i[0].values()])
        table.add_row(*[str(k) for k in i[1].values()], end_section=True)
    console.print(table)
