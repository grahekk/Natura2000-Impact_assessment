from PyQt5.QtCore import QVariant
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsExpression
from qgis.core import QgsApplication
from qgis.core import QgsProviderRegistry
from qgis.gui import *
from qgis import processing
from qgis.analysis import QgsNativeAlgorithms
from processing.core.Processing import Processing

# from conda_env.Library.python.qgis import processing

alg_provider = QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# for alg in QgsApplication.processingRegistry().algorithms():
#         print(alg.id(), "->", alg.displayName())


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
    bafer = processing.run('native:buffer', alg_params)['OUTPUT']
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
    Distance_matrix = Processing.run('qgis:distancematrix', alg_params)['OUTPUT']
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

    return print("Distances exported!")
