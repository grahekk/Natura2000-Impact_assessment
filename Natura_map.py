from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
import geopandas as gpd

# Define the WFS URL and the layer name
wfs_url = 'https://services.bioportal.hr/wms'

# Use owslib to get the data from the WFS
wfs11 = WebFeatureService(url=wfs_url, version='1.1.0')
wfs_contents = list(wfs11.contents)
layers_to_select = ['dzzpnpis:direktiva_o_stanistima_natura2000_hr_2019_',
                    'dzzpnpis:direktiva_o_pticama_natura2000_hr_2019_']

# select them layers
POVS_layer = wfs11.getfeature(typename=layers_to_select[0])
POP_layer = wfs11.getfeature(typename=layers_to_select[1])

# Use geopandas to convert the data to a GeoDataFrame
features = POVS_layer.json()['features']
geojson = {'type': 'FeatureCollection', 'features': features}
polygons = gpd.read_file(geojson=geojson)
polygons.plot()
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
