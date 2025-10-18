import argparse
import ndbduplicates as ndup

def parse_args():  
    """_Parse arguments if the script is run from the commandline._

    Returns:
        _argparse.Namespace_: _A Namespace object defining the argunments passed from the commandline._
    """  
    parser = argparse.ArgumentParser(prog = "Duplicate checker",
                                    description = "A Neotoma tool to help understand duplicate entries in Neotoma.")
    parser.add_argument('-t', '--table',
                        help='The table with duplicate values.',
                        type = str)
    parser.add_argument('-r', '--rows',
                        type = str,
                        help = 'Comma separated values for duplicate entries.')
    parser.add_argument('-s', '--schema',
                        default = 'ndb',
                        type = str,
                        help = 'The Neotoma Database schema in which the table is found (defaults to ndb).')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 1.0',
                        help='Show the program\'s version number and exit.')
    
    args = parser.parse_args()
    return args

def main(args):
    if not args.table:
        print('You must supply a valid Neotoma table name in the `ndb` schema.')
    print(f'Checking table "{args.table}".')
    if args.table:
        con = ndup.neo_connect()
        with con.cursor() as cur:
            with open('./src/sql/fk_tables.sql', 'r') as query:
                _ = cur.execute(query.read(), 
                                {'tablename': args.table,
                                 'schemaname': args.schema})
                tables = cur.fetchall()
                ndup.print_fk_tables(tables)
        if args.rows:
            rowval = ndup.parse_rows(args)
            result = []
            for i in tables:
                result.append([i, ndup.get_row_counts(con, 
                                                      schema = 'ndb',
                                                      table = i[1],
                                                      column = i[2],
                                                      rows = rowval)])
            ndup.print_row_results(result, rowval)

if __name__ == '__main__':
    args = parse_args()
    print(args)
else:
    # For testing in the Python environment:
    class args:
        table = 'taxa'
        rows = '1,2'
        schema = 'ndb'

main(args)
