__author__ = 'Kevin'

import gpxpy.parser as parser
import urllib2
import json
import time
import itertools
import glob

def build_url(coords, timestamp):
    url= "xxxxxxxxxx" #fill in server for OSRM match
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

for file in glob.glob("/gpx/*.gpx"):

    gpx_file = open('gpx/' + file, 'r' ) #fill in gpx to parse

    #parse gpx
    gpx_parser = parser.GPXParser( gpx_file )
    gpx_parser.parse()

    gpx_file.close()

    track = gpx_parser.gpx

    points = track.get_points_data()
    points.reverse()

    #initiate output arrays
    coords = []
    timestamp = []
    indices = []
    elevation = []

    i = 0
    f = open('output', 'w')

    keys = ['file_name','gpx_index','gpx_point_x', 'gpx_point_y', 'match_point_x', 'match_point_y', 'way_id', 'gpx_height']
    f.write(';'.join(keys) + '\n')

    for index, point in enumerate(points):
        #iterate in slices of 50 over gpx points
        #also check if the slice is smaller than 50 at the end of the gpx points array
        if i < 50 and index < len(points) - 1:
            coords.append((point.point.longitude,point.point.latitude))
            timestamp.append(int(time.mktime(point.point.time.timetuple())))
            indices.append(index)
            elevation.append(point.point.elevation)
            i += 1
        else:
            #fetch match based on slice
            i = 2
            url = build_url(coords, timestamp)
            print url
            result = fetch_result(url)
            tracepoints = result['tracepoints']
            #fetch output for json response
            for j,coord in enumerate(coords):
                if tracepoints[j] != None:
                    match = tracepoints[j]['location']
                    wayInfo = json.loads(tracepoints[j]['name'])
                    coord = {'file_name': file,'gpx_index':indices[j],'gpx_point_x':coord[0], 'gpx_point_y':coord[1], 'match_point_x':match[0], 'match_point_y':match[1], 'way_id':wayInfo[0], 'gpx_height':elevation[j]}
                    output = []
                    for key in keys:
                        output.append(str(coord[key]))
                    f.write(';'.join(output))
                    f.write('\n')
            #create overlap between slices to avoid missing end point in match
            coords = coords[-2:]
            timestamp = timestamp[-2:]
            indices = indices[-2:]
            elevation = indices[-2:]

