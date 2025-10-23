from psycopg2 import sql

def get_row_counts(con, table, column, rows, schema = 'ndb'):
    """_List row counts for the row identifiers._

    Args:
        con (_type_): _A valid connection to the database._
        schema (_type_): _A valid database schema._
        table (_type_): _A valid table with a foreign key to the parent table._
        column (_type_): _description_
        rows (_type_): _description_

    Returns:
        _type_: _description_
    """
    query = """with cte as (
                    select unnest(%(rowvals)s) as {colname}
               )
               SELECT %(schema)s as schema, %(table)s as table, %(colname)s as column, c.{colname}, COUNT(d.*) as count
               FROM cte as c
               LEFT OUTER JOIN {schemaname}.{tablename} AS d on d.{colname} = c.{colname}
               WHERE c.{colname} = ANY(%(rowvals)s)
               GROUP BY c.{colname};"""
    formatted = sql.SQL(query).format(schemaname=sql.Identifier(schema), tablename=sql.Identifier(table), colname=sql.Identifier(column), pkname=sql.Identifier('taxonid'))
    with con.cursor() as cur:
        cur.execute(formatted, {'rowvals': rows, 'schema': schema, 'table': table, 'colname': column})
        result=cur.fetchall()
    return result
