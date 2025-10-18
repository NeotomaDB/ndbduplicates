def show_counts(con, schema, table, rows):
    query = """SELECT COUNT(*)
               FROM {tablename}
               WHERE {pkname} = ANY(%(rowvals))"""