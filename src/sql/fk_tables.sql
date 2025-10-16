select distinct 
       fk_tco.table_schema || '.' || fk_tco.table_name as fk_table_name
from information_schema.referential_constraints rco
join information_schema.table_constraints fk_tco 
          on rco.constraint_name = fk_tco.constraint_name
          and rco.constraint_schema = fk_tco.table_schema
join information_schema.table_constraints pk_tco
          on rco.unique_constraint_name = pk_tco.constraint_name
          and rco.unique_constraint_schema = pk_tco.table_schema
where pk_tco.table_name = %(tablename)s
  and pk_tco.table_schema = %(schemaname)s
order by fk_table_name;