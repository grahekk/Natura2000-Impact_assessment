CREATE OR REPLACE FUNCTION calculate_forest_distance_raster(
    lon numeric,
    lat numeric,
    EPSG integer,
    schema_name text,
    table_name text,
    x_min numeric,
    y_min numeric,
    x_max numeric,
    y_max numeric)
RETURNS numeric
LANGUAGE plpgsql
AS $$
DECLARE
    result numeric;
    query text;
BEGIN

	query := format('
	SELECT ROUND(min(subq.st_distance)::numeric,2)
	FROM (
		WITH target_point AS (
			SELECT ST_Transform(
						ST_SetSRID(
							ST_MakePoint(%s, %s, %s),%s),
						3035) AS geom
		),
		pixel_polygons AS (
			SELECT (ST_DumpAsPolygons(rast)).geom AS geom 
			FROM %I.%I
			WHERE ST_Intersects(rast, ST_Transform(ST_MakeEnvelope(%s, %s, %s, %s, %s), 3035))	
		)
		SELECT
			ST_Distance(pixel_polygons.geom, target_point.geom),
			ST_ClusterDBSCAN(pixel_polygons.geom, eps := 1, minpoints := 1) OVER () AS cluster_id,
			ST_area(pixel_polygons.geom)
		FROM pixel_polygons, target_point
		ORDER BY ST_Distance(pixel_polygons.geom, target_point.geom)
		LIMIT 30
	) as subq
	GROUP BY subq.cluster_id
	HAVING SUM(subq.st_area)>10000
	LIMIT 1',
    lon, lat, EPSG, EPSG, schema_name, table_name, x_min, y_min, x_max, y_max, EPSG);
	
    -- Execute the dynamically generated query
    EXECUTE query INTO result;

    -- Return the calculated result
    RETURN result;
END;
$$;


-- SELECT calculate_forest_distance_raster (40.3630838, 40.8285381, 4326, 'satellite', 'europe_copernicus_forest_types_10m_v2_idx', 40.35119853955044, 40.819529090991, 40.374969060449565, 40.83754710900901)
