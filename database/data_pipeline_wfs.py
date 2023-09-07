import subprocess
from qgis.core import *
from decouple import config

# Read sensitive data from .env file
db_name = config('DB_NAME')
db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_host = config('DB_HOST')
db_port = config('DB_PORT')
wfs_url = config('WFS_URL')

table_name = 'your_table_name'
schema_name = 'schema_wfs'
gpkg_file_path = 'output.gpkg'

# Initialize QGIS application (make sure QGIS is installed and configured properly)
QgsApplication.setPrefixPath("/path/to/qgis/installation", True)
QgsApplication.initQgis()

# Step 1: Load WFS layer into QGIS project, fix it, and save it as GPKG
project = QgsProject.instance()
layer = QgsVectorLayer(wfs_url, "WFS Layer", "WFS")
if not layer.isValid():
    print("Error: Unable to load WFS layer.")
else:
    # Fix geometries (if necessary)
    layer.startEditing()
    QgsGeometryChecker().fixGeometry(layer)
    layer.commitChanges()

    # Rename the geometries column to "geom"
    layer.dataProvider().renameAttributes({0: 'geom'})

    # Save the layer as GPKG
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = 'GPKG'
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
    QgsVectorFileWriter.writeAsVectorFormatV2(layer, gpkg_file_path, options)

    print(f"WFS layer fixed and saved as GPKG: {gpkg_file_path}")

# Step 2: Use ogr2ogr to load GPKG file into PostGIS
ogr2ogr_command = [
    'ogr2ogr',
    '-f', 'PostgreSQL',
    f'PG:dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}',
    gpkg_file_path,
    '-nln', f'{schema_name}.{table_name}',
    '-overwrite',
    '-lco', 'OVERWRITE=YES',
    '-lco', 'SCHEMA=public',
    '-lco', 'GEOMETRY_NAME=geom',
    '-nlt', 'PROMOTE_TO_MULTI',
]

subprocess.run(ogr2ogr_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

print(f"GPKG data loaded into {table_name} in PostGIS.")

# Exit QGIS application
QgsApplication.exitQgis()
