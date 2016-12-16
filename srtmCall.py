__author__ = 'Kevin'

import urllib2
import xml.etree.ElementTree as ET
import sys
import json
import time

def fetch_result(url):
    count = 0
    while True:
        try:
            #fetch result from route json#
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            json_response = json.load(response)
            if 'error' in json_response:
                print "error in respons: " + json_response['error']
                print "retry after 5 seconds"
                time.sleep(5)
            else:
                return json_response
        except:
            #state how many loops you want. In this example 10
            if count < 10:
                count += 1
                print "failed to fetch respons -- retry after 5 seconds: " + str(count)
                time.sleep(5)
            else:
                print "failed to fetch respons"
                return {'result': None}


key = 'xxxxxxxxxxxxxxxx'

params = [key]

url = 'http://api.routeyou.com/3.0/json/Session?id=1&method=start&params=' + json.dumps(params)

token = fetch_result(url)['result']

#get height

#getPoint= input in wkt point
#params = {'point':{'wkt':"POINT(3.2 50.5)"}}

#getPoints: input is array van wkt point
params = {'points':[{'wkt':"POINT(3.2 50.5)"}, {'wkt':"POINT(3.5 51.2)"}]}

#url = 'http://api.routeyou.com/1.1/json/Srtm/' + token + '?id=1&method=fromPoint&params=' + json.dumps(params)
url = 'http://api.routeyou.com/1.1/json/Srtm/' + token + '?id=1&method=fromPoints&params=' + json.dumps(params)

print fetch_result(url)