def parse_rows(args):
    """_Parse row entries from the argument string._

    Args:
        args (_argparse.Namespace_): _A Namespace object passed from argparser.._

    Returns:
        _list_: _A list of integer values representing primary key IDs_
    """
    assert args.rows, "You must pass in Primary Key values for the table of interest."
    rows = [int(i) for i in args.rows.split(',')]
    assert all([int(i) > 0 for i in rows]), "All Primary key values must be positive integers > 0."
    assert len(rows) > 1, "To check for duplicates you must pass more than one Primary Key."
    return rows
