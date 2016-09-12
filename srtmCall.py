__author__ = 'Kevin'

import urllib2
import xml.etree.ElementTree as ET
import sys
import json

def fetch_result(url):
    #fetch result from route json#
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return json.load(response)

key = 'geef hier jouw key in'

params = [key]

url = 'http://api.routeyou.com/2.0/json/Session?id=1&method=start&params=' + json.dumps(params)

token = fetch_result(url)['result']

#get height

#getPoint= input in wkt point
#params = {'point':{'wkt':"POINT(3.2 50.5)"}}

#getPoints: input is array van wkt point
params = {'points':[{'wkt':"POINT(3.2 50.5)"}, {'wkt':"POINT(3.5 51.2)"}]}

#url = 'http://api.routeyou.com/1.1/json/Srtm/' + token + '?id=1&method=fromPoint&params=' + json.dumps(params)
url = 'http://api.routeyou.com/1.1/json/Srtm/' + token + '?id=1&method=fromPoints&params=' + json.dumps(params)

print fetch_result(url)