from PyQt5.QtCore import QVariant
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsExpression
import processing


def shortest_distance(main_layer, distance_layer):
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
    QgsProject.instance().addMapLayer(bafer)

    # Clip
    alg_params = {
        'INPUT': vlayer,
        'OVERLAY': bafer,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    clip = processing.run('native:clip', alg_params)['OUTPUT']
    clip.setName('Clip-buffer_EM')
    QgsProject.instance().addMapLayer(clip)

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
    QgsProject.instance().addMapLayer(points)

    # points along geometry for main layer
    alg_params = {
        'INPUT': main_layer,
        'DISTANCE': 10,
        'END_OFFSET': 0,
        'START_OFFSET': 0,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    main_points = processing.run('native:pointsalonglines', alg_params)['OUTPUT']
    QgsProject.instance().addMapLayer(main_points)

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
    QgsProject.instance().addMapLayer(Distance_matrix)

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
    QgsProject.instance().addMapLayer(Calculated)

    # unique values in the end
    alg_params = {
        'FIELDS': ['InputID', 'min_d'],
        'INPUT': Calculated,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    Unique_values = processing.run('qgis:listuniquevalues', alg_params)['OUTPUT']
    QgsProject.instance().addMapLayer(Unique_values)

    QgsProject.instance().removeMapLayer(vlayer)
    QgsProject.instance().removeMapLayer(bafer)
    QgsProject.instance().removeMapLayer(clip)
    QgsProject.instance().removeMapLayer(points)
    QgsProject.instance().removeMapLayer(main_points)
    QgsProject.instance().removeMapLayer(Distance_matrix)
    QgsProject.instance().removeMapLayer(Calculated)

    print("Distances exported!")
