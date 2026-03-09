SELECT
    *
FROM
    iris
LIMIT
    10;


-- sqlite_master is a special system table that sqlite automatically 
-- creates in every database. it stores the schema of the database
SELECT
    name
FROM
    sqlite_master
WHERE
    type = 'table';