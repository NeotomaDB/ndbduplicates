from .parse_rows import parse_rows
from psycopg2 import sql
from rich.console import Console
from rich.table import Table

def print_dup_rows(con, args):
    # First get the primary key:
    queryone = """SELECT c.column_name
                  FROM information_schema.table_constraints tc
                  JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
                  JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
                  AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
                  WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = %(tablename)s;"""
    with con.cursor() as cur:
        cur.execute(queryone, {'tablename': args.table})
        result=cur.fetchone()
    formatted = sql.SQL("""SELECT *
                           FROM {schemaname}.{tablename}
                           WHERE {pkname} = ANY(%(rowvals)s)
                        """).format(schemaname=sql.Identifier(args.schema),
                                    tablename=sql.Identifier(args.table),
                                    pkname=sql.Identifier(result['column_name']))
    with con.cursor() as cur:
        cur.execute(formatted, {'rowvals': parse_rows(args)})
        result=cur.fetchall()
    colnames = [key for key in result[0]]

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    for i in colnames:
        table.add_column(i, style = 'dim')
    for k in result:
        table.add_row(*[str(j) for j in k.values()])
    console.print(table)
    return result
