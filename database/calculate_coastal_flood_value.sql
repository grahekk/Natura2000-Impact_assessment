CREATE OR REPLACE FUNCTION osm.calculate_coastal_flood(
    lon numeric,
    lat numeric,
    EPSG integer,
    schema_name text,
    table_name text)
RETURNS numeric
LANGUAGE plpgsql
AS $$
DECLARE
    result numeric;
    query text;
BEGIN

	query := format('
	WITH point_coords AS (
					SELECT ST_SetSRID(
								ST_MakePoint(%s, %s), 
								%s)
					AS coords)
	SELECT min(sea_level)
	FROM %I.%I, point_coords
	WHERE ST_Intersects(
		point_coords.coords,
		%I.geom
	)',			
    lon, lat, EPSG, schema_name, table_name, table_name);
	
    -- Execute the dynamically generated query
    EXECUTE query INTO result;

    -- Return the calculated result
    RETURN result;
END;
$$;

-- example
-- SELECT * FROM osm.calculate_coastal_flood(-0.09373551514900187, 39.85208271958255, 4326, 'osm', 'europe_coastal_flood_10m')

