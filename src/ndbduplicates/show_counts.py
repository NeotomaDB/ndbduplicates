from .neo_connect import neo_connect
from .parse_rows import parse_rows
from .get_row_counts import get_row_counts
from .print_row_results import print_row_results

def show_counts(args):
    if args.table:
            con = neo_connect()
            with con.cursor() as cur:
                with open('./src/sql/fk_tables.sql', 'r') as query:
                    _ = cur.execute(query.read(),
                                    {'tablename': args.table,
                                    'schemaname': args.schema})
                    tables = cur.fetchall()
    if args.rows:
        rowval = parse_rows(args)
        result = []
        for i in tables:
            rowCount = get_row_counts(con,
                                            schema = 'ndb',
                                            table = i['table_name'],
                                            column = i['column_name'],
                                            rows = rowval)
            result.append([dict(j) for j in rowCount])
        print(f'** Checking the use of the duplicate row pair {args.rows} **')
        print_row_results(result, rowval)
