from .neo_connect import neo_connect
from psycopg2 import sql
from rich.console import Console
from rich.table import Table

def show_rows(args):
    assert args.schema
    assert args.table
    assert args.column
    assert args.query

    con = neo_connect()

    formatted = sql.SQL("""SELECT DISTINCT *
                           FROM {schemaname}.{tablename}
                           WHERE {colname} = %(query)s
                        """).format(schemaname=sql.Identifier(args.schema), 
                                    tablename=sql.Identifier(args.table),
                                    colname=sql.Identifier(args.column))
    with con.cursor() as cur:
        cur.execute(formatted, {'query': args.query})
        result=cur.fetchall()
    colnames = [key for key in result[0]]
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    for i in colnames:
        table.add_column(i, style = 'dim')
    for k in result:
        table.add_row(*[str(j) for j in k.values()])
    console.print(table)