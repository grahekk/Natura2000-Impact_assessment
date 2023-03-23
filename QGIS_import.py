import os
import sys
import json
import pandas as pd


# set up system paths
qspath = 'qgis_sys_paths.csv'
# provide the path where you saved this file.
paths = pd.read_csv(qspath).paths.tolist()
sys.path += paths
# set up environment variables
qepath = 'qgis_env.json'
js = json.loads(open(qepath, 'r').read())
for k, v in js.items():
    os.environ[k] = v

os.environ['PROJ_LIB'] = '/Applications/Qgis.app/Contents/Resources/proj'

sys.path.append(r'C:\Program Files\QGIS 3.22.8\apps\Python39\Lib')
sys.path.append(r'C:\Program Files\QGIS 3.22.8\apps')

import qgis.core
import PyQt5

# qgis library imports
import PyQt5.QtCore
import gdal
import qgis.PyQt.QtCore
from qgis.core import (QgsApplication,
                       QgsProcessingFeedback,
                       QgsProcessingRegistry)
from qgis.analysis import QgsNativeAlgorithms

feedback = QgsProcessingFeedback()
# initializing processing module
QgsApplication.setPrefixPath(js['HOME'], True)
qgs = QgsApplication([], False)
qgs.initQgis() # use qgs.exitQgis() to exit the processing module at the end of the script.
# initialize processing algorithms
from processing.core.Processing import Processing
Processing.initialize()
import processing
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

algs = dict()
for alg in QgsApplication.processingRegistry().algorithms():
    algs[alg.displayName()] = alg.id()
print(algs)