from PyQt5.QtXml import QDomDocument
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsPrintLayout, \
    QgsReadWriteContext, QgsLayoutExporter, QgsDataSourceUri


def set_project(project_path, crs):
    # Create a new project
    project = QgsProject.instance()
    project.clear()
    project.read(project_path)
    manager = project.layoutManager()
    # set project crs
    QgsProject.instance().setCrs(crs)
    return project, manager


def load_vector_layer(project, layer_name, geo_file, crs):
    # Load the map layer from the geo file
    layer = QgsVectorLayer(geo_file, layer_name, 'ogr')
    if layer.isValid():
        project.addMapLayer(layer)
        layer.setCrs(crs)
        return layer
    else:
        return print("Layer not valid!")


def load_raster_layer(project, layer_name, geo_file, crs):
    # Load the map layer from the geo file
    layer = QgsRasterLayer(geo_file, layer_name, 'ogr')
    if layer.isValid():
        project.addMapLayer(layer)
        layer.setCrs(crs)
        return layer
    else:
        return print("Layer not valid!")


def load_wms_layer(project, layer_name, layer_url, crs):
    # Load the map layer from the geo file
    layer = QgsRasterLayer(layer_url, layer_name, 'wms')
    if layer.isValid():
        project.addMapLayer(layer)
        layer.setCrs(crs)
        return layer
    else:
        return print("Layer not valid!")


def load_wfs_layer(project, layer_name, layer_url, crs):
    # Load the map layer from the geo file
    layer = QgsVectorLayer(layer_url, layer_name, 'wfs')
    if layer.isValid():
        project.addMapLayer(layer)
        layer.setCrs(crs)
        return layer
    else:
        return print("Layer not valid!")


def load_wfs_layer_from_uri(project, layer_url, feature_name, crs):
    # Load the map layer from the geo file
    uri = QgsDataSourceUri()
    uri.setParam('url', layer_url)
    uri.setParam('type', 'WFS')
    uri.setParam('version', '1.0.0')
    uri.setParam('typename', feature_name)
    layer = QgsVectorLayer(uri.uri(), feature_name, 'WFS')
    if layer.isValid():
        project.addMapLayer(layer)
        layer.setCrs(crs)
        return layer
    else:
        return print("Layer not valid!")


def open_template(project, manager, layer, dof_layer, layout_template, map_name):
    # Load the layout template
    layout = QgsPrintLayout(project)
    template_file = open(layout_template, encoding="utf-8")
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)
    layout.loadFromTemplate(document, QgsReadWriteContext())
    layout.setName(map_name)
    manager.addLayout(layout)

    # accessing layout items
    my_table = layout.items()

    # set map
    map = my_table[3]
    map.setLayers([layer, dof_layer])
    rect = layer.extent()
    RECTSCALE = 1.2
    rect.scale(RECTSCALE)
    map.zoomToExtent(rect)
    map.refresh()

    legend = my_table[0]
    root = legend.model().rootGroup()
    legendLyr = QgsProject.instance().mapLayersByName('EM')[0]
    root.addLayer(legendLyr)
    legend.refresh()

    scale = my_table[2]
    # set segment size to "fit the segment size"
    scale.setSegmentSizeMode(1)
    return layout


def export_image(layout, map_name, output_img_path):
    # Export the layout as image or jpg
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(output_img_path + map_name + '.jpg', exporter.ImageExportSettings())
    return print(f"{map_name} exported!")
