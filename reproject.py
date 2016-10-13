__author__ = 'Kevin'

from osgeo import ogr
from osgeo import osr

source = osr.SpatialReference()
source.ImportFromEPSG(4326)

target = osr.SpatialReference()
target.ImportFromEPSG(31370)

transform = osr.CoordinateTransformation(source, target)

point = ogr.CreateGeometryFromWkt("POINT (3.7815273 50.8319712)")
point.Transform(transform)

print point.ExportToWkt()