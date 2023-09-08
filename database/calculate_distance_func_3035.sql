CREATE OR REPLACE FUNCTION calculate_distance_func_3035(
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
    -- Create the query string with placeholders, function takes coordinates and envelope coordinates in 4326 and returns 3035
    query := format('
        WITH point_coords AS (
            SELECT ST_Transform(
                ST_SetSRID(
                    ST_MakePoint(%s, %s), 
                    %s), 
                3035) AS target
        )
        SELECT ROUND(
            min(
                ST_Distance(
                    geom, 
                    target)
                )::numeric, 2)
        FROM %I.%I, point_coords
        WHERE geom && ST_Transform(ST_MakeEnvelope(%s, %s, %s, %s, %s),3035)',
        lon, lat, EPSG, schema_name, table_name, x_min, y_min, x_max, y_max, EPSG);

    -- Execute the dynamically generated query
    EXECUTE query INTO result;

    -- Return the calculated result
    RETURN result;
END;
$$;

