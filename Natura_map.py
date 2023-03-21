import geopandas as gpd

# Load the GeoDataFrames
points = gpd.read_file("path/to/points.shp")
polygons = gpd.read_file("path/to/polygons.shp")

# Create a buffer around the points
buffered_points = points.buffer(distance=100)  # 100 is the buffer distance in the unit of the points' CRS

# Perform a spatial join between the polygons and the buffered points
selected_polygons = gpd.sjoin(polygons, buffered_points, op='intersects')
