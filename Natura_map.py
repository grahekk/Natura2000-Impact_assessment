import os

import geopandas as gpd
from owslib.wfs import WebFeatureService

dir = "geospatial_downloads"
if not os.path.exists(dir):
    os.mkdir(dir)


def get_natura_layer():
    # url from which the layers are downloaded
    wfs_url = 'https://services.bioportal.hr/wms'
    # natura layers to be downluaded from wfs
    layers_to_select = ['dzzpnpis:direktiva_o_stanistima_natura2000_hr_2019_',
                        'dzzpnpis:direktiva_o_pticama_natura2000_hr_2019_']
    # first check if the file already exists, and then make the request
    natura_layers = []
    for i, j in enumerate(layers_to_select):
        layer_to_select = layers_to_select[i]
        file_name = layer_to_select.split(":")[1]
        file = os.path.join(dir, file_name + ".kml")
        if not os.path.exists(f"{dir}/{file_name}.kml"):
            # Use owslib to get the data from the WFS
            wfs11 = WebFeatureService(url=wfs_url, version='1.1.0')
            # select them layers and get the response
            response = wfs11.getfeature(typename=layer_to_select)
            with open(file, 'wb') as f:
                f.write(response.read())
            print(f"{file_name} downloaded.")
        else:
            print(f"{file_name} already exists, skipping download")
        natura_layers.append(file)
    return natura_layers


layers = get_natura_layer()
# read the polygons
polygons = gpd.read_file(layers[0], crs='EPSG:3765')
polygons.plot()

# extract by the location part
# Load the main shp
points = gpd.read_file("path/to/points.shp")

# Create a buffer around the points
buffered_points = points.buffer(distance=100)  # 100 is the buffer distance in the unit of the points' CRS

# Perform a spatial join between the polygons and the buffered points
selected_polygons = gpd.sjoin(polygons, buffered_points, op='intersects')
