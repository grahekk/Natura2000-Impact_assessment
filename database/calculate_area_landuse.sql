CREATE OR REPLACE FUNCTION calculate_landuse_area_percentage(
    x_min double precision,
    y_min double precision,
    x_max double precision,
    y_max double precision,
    epsg integer,
    schema_name text,
    table_name text
)
RETURNS TABLE (percentage numeric(3, 2), label_climatig varchar(100)) 
AS $$
DECLARE
	result numeric;
	dynamic_query text;
BEGIN
	dynamic_query := format('
		WITH percentages AS (
			WITH bbox AS (
				SELECT ST_Transform(ST_MakeEnvelope(%s, %s, %s, %s, %s), 3035) AS geom
			)
			SELECT
				code_18, 
				(ST_Area(ST_Intersection(features.geom, bbox.geom)) / ST_Area(bbox.geom)) * 100 AS percentage
			FROM
				%I.%I AS features,
				bbox
			WHERE
				ST_Intersects(features.geom, bbox.geom)
		)
		SELECT ROUND(CAST (SUM(p.percentage) as numeric),2), legend.label_climatig
		FROM percentages p
		RIGHT JOIN osm.europe_copernicus_clc2018_legend AS legend
		ON p.code_18 = legend.clc_code
		GROUP BY legend.label_climatig, legend.climatig_code
		ORDER BY legend.climatig_code::integer;',
		x_min, y_min, x_max, y_max, epsg, schema_name, table_name);

-- 		RAISE NOTICE 'Dynamic Query: %', dynamic_query;
	-- Execute the dynamically generated query
    RETURN QUERY EXECUTE dynamic_query;

END;
$$ LANGUAGE plpgsql;

-- DROP FUNCTION calculate_landuse_area_percentage