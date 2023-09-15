CREATE OR REPLACE FUNCTION calculate_get_pixel_value(
    lon numeric,
    lat numeric,
    EPSG_in integer,
    EPSG_out integer,
    schema_name text,
    table_name text)
	
RETURNS numeric
LANGUAGE plpgsql
AS $$
DECLARE
    result numeric;
    query text;
BEGIN
	-- function that fetches the pixel value from raster for a given point in lat, lon coordinates in epsg 4326
	query := format('

	SELECT 
		ST_Value(rast, ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), %s), %s)) AS pixel_value
	FROM 
		%I.%I
	WHERE 
		ST_Intersects(rast, ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), %s), %s))',
    	lon, lat, EPSG_in, EPSG_out, schema_name, table_name, lon, lat, EPSG_in, EPSG_out);

   -- Execute the dynamically generated query
    EXECUTE query INTO result;

    -- Return the calculated result
    RETURN result;
END;
$$;

-- SELECT calculate_get_pixel_value(40.3730838, 40.8285381, 4326, 3035, 'osm', 'europe_copernicus_forest_types_10m_v2_idx')
