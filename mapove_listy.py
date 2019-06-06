from qgis.processing import alg
from qgis.core import QgsFeature, QgsFeatureSink, QgsFeature, QgsPointXY, QgsGeometry, QgsProject, QgsFields, QgsField, QgsWkbTypes
import math
import processing
from PyQt5.QtCore import QVariant

@alg(name="Create map tiles", label="Map tiles", group="MT", group_label="MT")
@alg.input(type=alg.SOURCE, name="INPUT", label="Input layer")
@alg.input(type=alg.NUMBER, name="WIDTH", label="Width", default=600)
@alg.input(type=alg.NUMBER, name="HEIGHT", label="Heigth", default=400)
@alg.input(type=alg.NUMBER, name="EXTRA", label="Extra width and height", default=5)
@alg.input(type=alg.SINK, name="OUTPUT", label="Output layer")
def ml(instance, parameters, context, feedback, inputs):
    """
    Tool for creating of map layers based on input point layer
    """
    feedback.pushInfo("Creating map tiles")
    feedback.pushInfo("Inicialization of inputs")
    feedback.setProgress(0)

    width = instance.parameterAsDouble(parameters, "WIDTH", context)
    height = instance.parameterAsDouble(parameters, "HEIGHT", context)
    extra = instance.parameterAsDouble(parameters, "EXTRA", context)

    source = instance.parameterAsSource(parameters, "INPUT", context)

    fields = QgsFields()
    fields.append(QgsField("PageNumber", QVariant.Int))

    (sink, dest_id) = instance.parameterAsSink(parameters, "OUTPUT", context, fields, QgsWkbTypes.Polygon, source.sourceCrs())
    
    center = {'x': width / 2, 'y': height / 2}

    feedback.pushInfo("Setting bounds")
    feedback.setProgress(10)

    box = QgsFeature().geometry().boundingBox()
    for feature in source.getFeatures():
        box.combineExtentWith(feature.geometry().boundingBox())
    
    box = box.buffered(extra)

    count = {
        'x': abs(math.floor((box.xMinimum() - box.xMaximum()) / width)),
        'y': abs(math.ceil((box.yMaximum() - box.yMinimum()) / height))
         }

    half_sizes = { 'width': width / 2, 'height': height / 2 }

    polygons = []

    center = {'x': 0, 'y': 0}

    feedback.setProgress(20)
    number_of_tiles =   count['x'] * count['y']  
    feedback.pushInfo("Looping through " + str(number_of_tiles) + " tiles")
    pageNumber = 1

    if count['x'] % 2 == 0:
        center['x'] = box.center().x() - ((count['x'] /2) * width) + half_sizes['width']
    elif count['x'] == 0:
        box.center().x()
    else:
        center['x'] = box.center().x() - ((math.floor(count['x'] / 2)) * width)

    if count['y'] % 2 == 0:
        center['y'] = box.center().y() + (((count['y'] / 2) - 1) * height) + half_sizes['height']
    elif count['y'] == 0:
        box.center().y()
    else:
        center['y'] = box.center().y() + ((math.floor(count['y'] / 2)) * height)

    feedback.setProgress(30)
    i = 0
    for i_y in range(0, count['y']):
        y = center['y'] - i_y * height

        for i_x in range(0, count['x']):
            i += 1

            feedback.setProgress(i / number_of_tiles * 70 + 30)
            x = center['x'] + i_x * width

            poly = QgsFeature()
            points = [
                QgsPointXY(x - half_sizes['width'], y - half_sizes['height']),
                QgsPointXY(x - half_sizes['width'], y + half_sizes['height']),
                QgsPointXY(x + half_sizes['width'], y + half_sizes['height']),
                QgsPointXY(x + half_sizes['width'], y - half_sizes['height'])
                ]
            poly.setGeometry(QgsGeometry.fromPolygonXY([points]))

            for feature in source.getFeatures(): 
                if poly.geometry().intersects(feature.geometry()):
                    poly.setAttributes([pageNumber])
                    pageNumber += 1
                    polygons.append(poly)
                    break

    sink.addFeatures(polygons)

    feedback.setProgress(100)
    feedback.pushInfo("Generating of map tiles ended.")

    return {"OUTPUT": "Created " + str(pageNumber - 1) + " tiles"}
