CREATE OR REPLACE FUNCTION get_closest_point_coordinates_3035(
    lon numeric,
    lat numeric,
    EPSG integer,
    schema_name text,
    table_name text,
    x_min numeric,
    y_min numeric,
    x_max numeric,
    y_max numeric)
RETURNS TABLE (closest_lon double precision, closest_lat double precision)
LANGUAGE plpgsql
AS $$
DECLARE
    query text;
BEGIN
    -- Create the query string with placeholders, function takes coordinates and envelope coordinates in 4326 and returns 3035
    query := format('
        WITH point_coords AS (
            SELECT 
                ST_Transform(
                    ST_SetSRID(
                        ST_MakePoint(%s, %s), 
                        %s),
                    3035) AS target
        )
        SELECT 
            ST_X(ST_transform(
                ST_ClosestPoint(
                    geom, 
                    target), 
                %s)) AS closest_lon,
            ST_Y(ST_transform(
                ST_ClosestPoint(
                    geom, 
                    target),
                %s)) AS closest_lat
        FROM %I.%I, point_coords
        WHERE geom && ST_Transform(ST_MakeEnvelope(%s, %s, %s, %s, %s), 3035)        
		ORDER BY ST_Distance(geom, target)
        LIMIT 1',
        lon, lat, EPSG, EPSG, EPSG, schema_name, table_name, x_min, y_min, x_max, y_max, EPSG);

    RETURN QUERY EXECUTE query;

END;
$$;

