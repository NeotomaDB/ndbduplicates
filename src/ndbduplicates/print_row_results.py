from rich.console import Console
from rich.table import Table

def print_row_results(rowresults, rows):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Related Schema", style="dim")
    table.add_column("Related Table", style="dim")
    table.add_column("Related Column", style="dim")
    table.add_column("Row Value", style="dim")
    table.add_column("Count", style="dim")
    for i in rowresults:
        for j in i[:-1]:
            table.add_row(*[str(k) for k in j.values()])
        table.add_row(*[str(k) for k in i[-1].values()], end_section=True)
    console.print(table)
