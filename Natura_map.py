import geopandas as gpd

# Define the WFS URL and the layer name
wfs_url = 'https://services.bioportal.hr/wfs'
layer_name = 'example_layer'

# Use geopandas to get the available layers on the WFS
wfs_layers = gpd.read_file(wfs_url, driver='WFS')

# Print the layer names
print(wfs_layers['Name'])

# Use geopandas to load the data from the WFS
polygons = gpd.read_file(wfs_url, layer=layer_name, crs='EPSG:3765')

# Load the GeoDataFrames
points = gpd.read_file("path/to/points.shp")
polygons = gpd.read_file("path/to/polygons.shp")

# Create a buffer around the points
buffered_points = points.buffer(distance=100)  # 100 is the buffer distance in the unit of the points' CRS

# Perform a spatial join between the polygons and the buffered points
selected_polygons = gpd.sjoin(polygons, buffered_points, op='intersects')
