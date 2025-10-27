import argparse
import ndbduplicates as ndup

def parse_args():  
    """_Parse arguments if the script is run from the commandline._

    Returns:
        _argparse.Namespace_: _A Namespace object defining the argunments passed from the commandline._
    """  
    parser = argparse.ArgumentParser(prog = "Duplicate checker",
                                     description = "A Neotoma tool to help understand duplicate entries in Neotoma.",
                                     )
    parser.add_argument('tool',
                        nargs = 1,
                        help = 'The name of the ndbduplicates tool to be used.',
                        choices=['show_rows', 'show_keys', 'show_counts', 'keep_id'])
    parser.add_argument('-s', '--schema',
                        default = 'ndb',
                        type = str,
                        help = 'The Neotoma Database schema in which the table is found (defaults to ndb).')
    parser.add_argument('-t', '--table',
                        help='The table with duplicate values.',
                        type = str)
    parser.add_argument('-c', '--column',
                        type = str,
                        help = 'The Neotoma Database schema in which the table is found (defaults to ndb).')
    parser.add_argument('-q', '--query',
                        type = str,
                        help = 'Term to match in table (defined by -t). By default we use `=` to check equality.')
    parser.add_argument('-r', '--rows',
                        type = str,
                        help = 'Comma separated values for duplicated entries.')
    parser.add_argument('-k', '--keep',
                        type = int,
                        help = 'Keep row entry.')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 1.0',
                        help='Show the program\'s version number and exit.')
    
    args = parser.parse_args()
    return args

def main(args):
    if not args.table:
        print('You must supply a valid Neotoma table name in the `ndb` schema.')
    
    if args.tool[0] == 'show_rows':
        ndup.show_rows(args)

    if args.tool[0] == 'show_keys':
        print(f'** Checking the use of "{args.table}''s" Primary Key **')
        if args.table:
            con = ndup.neo_connect()
            with con.cursor() as cur:
                with open('./src/sql/fk_tables.sql', 'r') as query:
                    _ = cur.execute(query.read(), 
                                    {'tablename': args.table,
                                    'schemaname': args.schema})
                    tables = cur.fetchall()
                    ndup.print_fk_tables(tables)
    
    if args.tool[0] == 'keep_id':
        if args.table:
            con = ndup.neo_connect()
            with con.cursor() as cur:
                with open('./src/sql/fk_tables.sql', 'r') as query:
                    _ = cur.execute(query.read(), 
                                    {'tablename': args.table,
                                    'schemaname': args.schema})
                    tables = cur.fetchall()
                # We're replacing values and keeping one of them.
        rowval = ndup.parse_rows(args)
        assert args.keep, "You must define a PK value to keep when asking to keep values."
        assert args.keep in rowval, "The value to keep must be in the set of row values provided."
    if args.tool[0] == 'show_counts':
        if args.table:
            con = ndup.neo_connect()
            with con.cursor() as cur:
                with open('./src/sql/fk_tables.sql', 'r') as query:
                    _ = cur.execute(query.read(), 
                                    {'tablename': args.table,
                                    'schemaname': args.schema})
                    tables = cur.fetchall()
        if args.rows:
            rowval = ndup.parse_rows(args)
            result = []
            for i in tables:
                rowCount = ndup.get_row_counts(con, 
                                                schema = 'ndb',
                                                table = i['table_name'],
                                                column = i['column_name'],
                                                rows = rowval)
                result.append([dict(j) for j in rowCount])
            print('\n')
            print(f'** Checking the use of the duplicate row pair {args.rows} **')
            ndup.print_row_results(result, rowval)

if __name__ == '__main__':
    args = parse_args()
else:
    # For testing in the Python environment:
    class args:
        table = 'taxa'
        rows = '1,2'
        schema = 'ndb'
        tool = 'show_rows'

print('*** Neotoma Duplicate Investigator ***')
print('Running with user defined variables:')
for j, k in vars(args).items():
    print(f'\t{j}: {k}')
print('\n')
main(args)
