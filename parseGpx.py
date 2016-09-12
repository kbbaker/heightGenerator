__author__ = 'Kevin'

import gpxpy.parser as parser
import urllib2
import json
import time
import itertools

def build_url(coords, timestamp):

    url= "https://router.project-osrm.org/match/v1/driving/"
    location = "%s,%s"
    locations = []
    for coord in coords:
        locations.append(location%(coord[0],coord[1]))
    url += ';'.join(locations)
    #print ','.join(map(str,timestamp))
    param = "?timestamps=" + ';'.join(map(str,timestamp))
    url += param
    return url

def fetch_result(url):
    #fetch result from route json#
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    result = json.load(response)

    return result

gpx_file = open('gpx/1701466(15390316)', 'r' )

gpx_parser = parser.GPXParser( gpx_file )
gpx_parser.parse()

gpx_file.close()

track = gpx_parser.gpx

points = track.get_points_data()
points.reverse()
coords = []
timestamp = []

i = 0
for point in points:
    if i < 100:
        coords.append((point.point.longitude,point.point.latitude))
        timestamp.append(int(time.mktime(point.point.time.timetuple())))
        i += 1
    else:
        i = 0
        url = build_url(coords, timestamp)
        result = fetch_result(url)
        tracepoints = result['tracepoints']
        for j,coord in enumerate(coords):
            print coord, tracepoints[j]
        coords = []
        timestamp = []

