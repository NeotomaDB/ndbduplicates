SELECT {pkname}, COUNT(*)
FROM {tablename}
WHERE {pkname} = ANY(%(rowvals))
