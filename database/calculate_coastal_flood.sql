CREATE OR REPLACE FUNCTION osm.calculate_coastal_flood(
    lon numeric,
    lat numeric,
    EPSG_in integer,
	EPSG_out integer,
    schema_name text,
    table_name text)
RETURNS TABLE (distance numeric(5, 2), sea_level double precision) 
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
	SELECT CASE 
		WHEN (ST_within(coords, geom)) THEN 0
		WHEN (SELECT osm.is_within(%s, %s, %s, ''%I'', ''world_seas''))=1 THEN 0
		ELSE ROUND(ST_distance(ST_Transform(point_coords.coords, %s), ST_Transform(%I.geom, %s))::numeric,2)
		END AS distance,
		CASE 
		WHEN (ST_within(coords, geom)) THEN min(sea_level) END as sea_level
	FROM %I.%I, point_coords
	WHERE ST_DWithin(point_coords.coords, %I.%I.geom, 0.001)
	GROUP BY point_coords.coords, %I.geom
	ORDER BY distance asc
	LIMIT 1',			
    lon, lat, EPSG_in, lon, lat, EPSG_in, schema_name, EPSG_out, table_name, EPSG_out, schema_name, table_name, schema_name, table_name, table_name);
	
    -- Execute the dynamically generated query
    RETURN QUERY EXECUTE query;

END;
$$;

-- example
-- SELECT osm.calculate_coastal_flood(14.363596846897448, 45.342087557485016, 4326, 3035, 'osm', 'europe_coastal_flood_10m')

