select distinct
       fk_tco.constraint_schema,
       fk_tco.table_name,
       kcu.column_name
from information_schema.referential_constraints rco
left join information_schema.table_constraints fk_tco
          on rco.constraint_name = fk_tco.constraint_name
          and rco.constraint_schema = fk_tco.table_schema
join information_schema.table_constraints pk_tco
          on rco.unique_constraint_name = pk_tco.constraint_name
          and rco.unique_constraint_schema = pk_tco.table_schema
join information_schema.key_column_usage kcu
		  on fk_tco.constraint_name = kcu.constraint_name
where pk_tco.table_name = %(tablename)s
  and pk_tco.table_schema = %(schemaname)s
order by fk_tco.table_name;
