from PyQt5.QtXml import QDomDocument
from qgis.core import QgsApplication, QgsProject, QgsCoordinateReferenceSystem, QgsVectorLayer, QgsPrintLayout, \
    QgsReadWriteContext, QgsLayoutExporter, QgsProviderRegistry
import os
import time

from QGIS_export_map import *

start = time.time()
# Provide the path to inputs: the geo file and template
geo_file = "C:/Users/Nikola/Documents/GitHub/Natura2000-Impact_assessment/EIA_app/uploaded_files/rendom_test.kml"
layout_template = "C:/Users/Nikola/Documents/GitHub/QGIS_mapping_automatization/styles_layouts/EM.qpt"
# outputs
output_img_path = "C:/Users/Nikola/Documents/GitHub/Natura2000-Impact_assessment/EIA_app/processing_output/"
qgis_prefix_path = os.environ['QGIS_PREFIX_PATH']

map_name = "EM"

# Start the QGIS application
QgsApplication.setPrefixPath(qgis_prefix_path, True)
qgs = QgsApplication([], False, platformName="desktop")
qgs.initQgis()

project_path = "project.qgz"
my_crs = QgsCoordinateReferenceSystem("EPSG:3765")

# exporting the image
project = set_project(project_path, my_crs)[0]
manager = set_project(project_path, my_crs)[1]
layers = load_layers(project, geo_file, my_crs)
layer = layers[0]
dof_layer = layers[1]
layout = open_template(project, manager, layer, dof_layer, layout_template, map_name)
export_image(layout, map_name, output_img_path)

# Exit the QGIS application
qgs.exitQgis()

end = time.time()
print(end - start, " seconds")
