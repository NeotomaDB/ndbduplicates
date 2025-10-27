UPDATE {schemaname}.{tablename}
SET {fkname}=%(keepvalue)
WHERE {fkname}=%(oldvalue)
ON CONFLICT DO NOTHING;