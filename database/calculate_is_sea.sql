CREATE OR REPLACE FUNCTION is_within(
    lon numeric,
    lat numeric,
    EPSG integer,
    schema_name text,
    table_name text)
RETURNS SETOF integer
LANGUAGE plpgsql
AS $$
DECLARE
    query text;
BEGIN
    -- Create the dinamic query string with placeholders
    query := format('
		   WITH point_coords AS (
				SELECT ST_SetSRID(
					ST_MakePoint(%s, %s), 
					%s) 
				AS coords)
            SELECT CASE WHEN ST_within(coords, geom) THEN 1 ELSE 0 END AS point_status
            FROM %I.%I, point_coords
            WHERE ST_within(coords, geom)',
        lon, lat, EPSG, schema_name, table_name);

    RETURN QUERY EXECUTE query;

END;
$$;

--DROP FUNCTION get_closest_point_coordinates;

--SELECT get_closest_point_coordinates({lon}, {lat}, {EPSG}, 'osm', 'world_seas', {x_min}, {y_min}, {x_max}, {y_max});
--SELECT * FROM get_closest_point_coordinates(-6.2603,53.3498, 4326, 'osm', 'world_lakes', -6.862922735007048, 52.98943963963964, -5.657677264992952, 53.71016036036036);
--SELECT * FROM get_closest_point_coordinates(17.979171,42.743809, 4326, 'osm', 'world_seas', 17.48934503973629, 42.38344863963964, 18.468996960263716, 43.10416936036036);
