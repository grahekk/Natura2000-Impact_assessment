CREATE OR REPLACE FUNCTION calculate_forest_distance_raster(
    lon numeric,
    lat numeric,
    EPSG_in integer,
    EPSG_out integer,
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
	WITH target_point AS (
		SELECT ST_Transform(
			ST_SetSRID(
				ST_MakePoint(%s, %s, %s),
				%s
			),
			%s
		) AS point_geom
	),
	pixel_polygons AS (
		SELECT
			(ST_DumpAsPolygons(rast)).geom AS geom,
			(ST_DumpAsPolygons(rast)).val AS val
		FROM %I.%I
		WHERE ST_Intersects(
			rast,
			ST_Transform(
				ST_MakeEnvelope(%s, %s, %s, %s, %s),
				%s
			)
		)
	),
	clustered_polygons AS (
		SELECT
			pixel_polygons.geom AS polygon_geom,
			pixel_polygons.val AS polygon_val,
			ST_ClusterDBSCAN(pixel_polygons.geom, eps := 10, minpoints := 1) OVER () AS cluster_id
		FROM pixel_polygons, target_point
		WHERE pixel_polygons.val IN (1,2)
	)
	SELECT
	--     cluster_id,
	--     ST_AsText(ST_Collect(polygon_geom)) AS cluster_centroid,
	-- 		max(polygon_val) as dn_digitalnumber,
	--     SUM(ST_Area(polygon_geom)) AS cluster_area,
		ROUND(MIN(ST_Distance(target_point.point_geom, polygon_geom))::numeric, 2) AS min_distance
	FROM clustered_polygons, target_point
	GROUP BY cluster_id, target_point.point_geom
	HAVING SUM(ST_Area(polygon_geom)) > 10000
	ORDER BY min_distance
	LIMIT 1',
    lon, lat, EPSG_in, EPSG_in, EPSG_out, schema_name, table_name, x_min, y_min, x_max, y_max, EPSG_in, EPSG_out);
	
    -- Execute the dynamically generated query
    EXECUTE query INTO result;

    -- Return the calculated result
    RETURN result;
END;
$$;


-- SELECT calculate_forest_distance_raster (40.3630838, 40.8285381, 4326, 3035, 'satellite', 'europe_copernicus_forest_types_10m_v2_idx', 40.35119853955044, 40.819529090991, 40.374969060449565, 40.83754710900901)
