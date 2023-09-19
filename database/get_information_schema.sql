-- SELECT columns and tables
SELECT 
   table_name, 
   ARRAY_AGG(ROW(column_name, data_type)::text) AS columns_and_data_types
FROM 
   information_schema.columns
WHERE 
   table_schema = 'osm'
GROUP BY table_name;

   

-- SELECT functions and their arguments
SELECT 
    routine_name AS function_name,
    routines.data_type AS return_type,
    array_agg(parameters.data_type) AS argument_types
FROM 
    information_schema.routines
LEFT JOIN
    information_schema.parameters
ON 
    routines.specific_name = parameters.specific_name
WHERE 
	routine_schema LIKE 'osm'
GROUP BY
    routine_name, routines.data_type
ORDER BY
    routine_name;



