from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsPrintLayout,
    QgsReadWriteContext,
    QgsLayoutExporter,
    QgsProviderRegistry,
    QgsProcessing,
    QgsProcessingProvider,
    QgsProcessingFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingOutputRasterLayer,
    QgsProcessingOutputMapLayer,
    QgsField,
    QgsDataSourceUri)
# from qgis.gui import *


import os
import time
import sys
from QGIS_export_map import *
# from QGIS_export_distances import shortest_distance

start = time.time()
# Provide the path to inputs: the geo file and template
geo_file = "C:/Users/Nikola/Documents/GitHub/Natura2000-Impact_assessment/EIA_app/uploaded_files/rendom_test.kml"
layout_template = "C:/Users/Nikola/Documents/GitHub/QGIS_mapping_automatization/styles_layouts/EM.qpt"
# outputs
output_img_path = "C:/Users/Nikola/Documents/GitHub/Natura2000-Impact_assessment/EIA_app/processing_output/"
qgis_prefix_path = os.environ['QGIS_PREFIX_PATH']

PATH_POVS = "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:3765' typename='dzzpnpis:direktiva_o_stanistima_natura2000_hr_2019_' url='http://services.bioportal.hr/wms' version='auto'"
PATH_POP = "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:3765' typename='dzzpnpis:direktiva_o_pticama_natura2000_hr_2019_' url='http://services.bioportal.hr/wms' version='auto'"
PATH_DOF = "contextualWMSLegend=0&crs=EPSG:3765&dpiMode=7&featureCount=10&format=image/png&layers=DOF&styles&url=http://geoportal.dgu.hr/wms?layers%3DDOF"

MAP_NAME = "EM"
MAIN_LAYER_NAME = MAP_NAME


# Start the QGIS application
QgsApplication.setPrefixPath(qgis_prefix_path, True)
qgs = QgsApplication([], False, platformName="desktop")
qgs.initQgis()

# and then processing
from qgis.analysis import QgsNativeAlgorithms
import processing
from processing.core.Processing import Processing
from processing.core.ProcessingConfig import ProcessingConfig

Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# set the project stuff
project_path = "project.qgz"
my_crs = QgsCoordinateReferenceSystem("EPSG:3765")

# exporting the image
project = set_project(project_path, my_crs)[0]
manager = set_project(project_path, my_crs)[1]
main_layer = load_vector_layer(project, MAIN_LAYER_NAME, geo_file, my_crs)
dof_layer = load_wms_layer(project, 'dof', PATH_DOF, my_crs)


# layout = open_template(project, manager, main_layer, dof_layer, layout_template, MAP_NAME)
# export_image(layout, MAP_NAME, output_img_path)

def shortest_distance(main_layer, distance_layer, project):
    # KS buffer clip
    # Buffer
    alg_params = {
        'DISSOLVE': True,
        'DISTANCE': 2000,
        'END_CAP_STYLE': 0,
        'INPUT': main_layer,
        'JOIN_STYLE': 0,
        'MITER_LIMIT': 2,
        'SEGMENTS': 5,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    feedback = QgsProcessingFeedback()
    bafer = processing.run('native:buffer', alg_params, feedback=feedback)['OUTPUT']
    project.addMapLayer(bafer)

    # Clip
    alg_params = {
        'INPUT': distance_layer,
        'OVERLAY': bafer,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    clip = processing.run('native:clip', alg_params)['OUTPUT']
    clip.setName('Clip-buffer_EM')
    project.addMapLayer(clip)

    # onda ide point along geometry x2
    # Points along geometry
    alg_params = {
        'INPUT': clip,
        'DISTANCE': 10,
        'END_OFFSET': 0,
        'START_OFFSET': 0,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    points = processing.run('native:pointsalonglines', alg_params)['OUTPUT']
    project.addMapLayer(points)

    # points along geometry for main layer
    alg_params = {
        'INPUT': main_layer,
        'DISTANCE': 10,
        'END_OFFSET': 0,
        'START_OFFSET': 0,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    main_points = processing.run('native:pointsalonglines', alg_params)['OUTPUT']
    project.addMapLayer(main_points)

    # adding new field to main_points
    provider = main_points.dataProvider()
    id_field = QgsField("n_id", QVariant.Double)
    provider.addAttributes([id_field])
    main_points.updateFields()

    alg_params = {
        'INPUT': points,
        'INPUT_FIELD': 'sitename',
        'MATRIX_TYPE': 0,
        'NEAREST_POINTS': 1,
        'TARGET': main_points,
        'TARGET_FIELD': 'n_id',
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    Distance_matrix = processing.run('qgis:distancematrix', alg_params)['OUTPUT']
    project.addMapLayer(Distance_matrix)

    # field calc minimum(min(Distance), InputID)
    # provider = Distance_matrix.dataProvider()
    # Min_distance = QgsField("min_d", QVariant.Double)
    # provider.addAttributes([Min_distance])
    # Distance_matrix.updateFields()

    # Field calculator
    alg_params = {
        'FIELD_LENGTH': 10,
        'FIELD_NAME': 'min_d',
        'FIELD_PRECISION': 3,
        'FIELD_TYPE': 0,  # Float
        'FORMULA': 'round(minimum(min(Distance), InputID),3)',
        'INPUT': Distance_matrix,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    Calculated = processing.run('native:fieldcalculator', alg_params)['OUTPUT']
    project.addMapLayer(Calculated)

    # unique values in the end
    alg_params = {
        'FIELDS': ['InputID', 'min_d'],
        'INPUT': Calculated,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    Unique_values = processing.run('qgis:listuniquevalues', alg_params)['OUTPUT']
    project.addMapLayer(Unique_values)

    project.removeMapLayer(distance_layer)
    project.removeMapLayer(bafer)
    project.removeMapLayer(clip)
    project.removeMapLayer(points)
    project.removeMapLayer(main_points)
    project.removeMapLayer(Distance_matrix)
    project.removeMapLayer(Calculated)
    print("distances exported!")
    return Unique_values


# shortest distances
BIOPORTAL_URL = 'http://services.bioportal.hr/wms'
feature_name = 'dzzpnpis:direktiva_o_pticama_natura2000_hr_2019_'

# Create the vector layer
pop_layer = load_wfs_layer_from_uri(project, BIOPORTAL_URL, feature_name, my_crs)
print(pop_layer)
distances_POVS = shortest_distance(main_layer, pop_layer, project)

features = distances_POVS.getFeatures()
pop_layer

# Iterate over the features
for feature in features:
    # Access the attributes of the feature
    attributes = feature.attributes()

    # Print the attributes
    for attribute in attributes:
        print(attribute)

# Exit the QGIS application
qgs.exitQgis()

end = time.time()
print(end - start, " seconds")
