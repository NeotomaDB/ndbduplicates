from rich.console import Console
from rich.table import Table
from itertools import chain

def print_row_results(rowresults, rows):
    print('***')
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Related Schema", style="dim")
    table.add_column("Related Table", style="dim")
    table.add_column("Related Column", style="dim")
    table.add_column(f"RowID {rows[0]}", style="dim")
    table.add_column(f"RowID {rows[1]}", style="dim")
    outcome = []
    for i in rowresults:
        result = [k for k in i[0]]
        rowResult = dict((x, y) for x, y in i[1])
        counts = ([[v for k,v in rowResult.items() if str(k) == str(y)] or 0 for y in rows])
        for z in counts:
            if type(z) is list:
                result.append(str(z[0]))
            else:
                result.append(str(z))
        outcome.append(result)
    for i in outcome:
        table.add_row(i[0], i[1], i[2], i[3], i[4])
    console.print(table)