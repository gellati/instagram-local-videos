#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
from flask import Flask, request, jsonify, make_response, current_app
from datetime import timedelta
from functools import update_wrapper

access_token = '1555940494.e029fea.f4f3539e108d4079b960d11199a97a9f'
client_secret = '715faafee65a4a7eb498c216adc72771'

baseUrl = "https://api.instagram.com/v1"

app = Flask(__name__)


def crossdomains(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def getNearbyLocationIds(lat, lng):
    r = requests.get(baseUrl + "/locations/search?lat=" + lat + "&lng=" + lng + "&access_token=" + access_token)
    if(r.ok):
        ids = []
        print r.status_code
        data = json.loads(r.text)
        for d in data['data']:
            if int(d['id']) != 0:
                print d['id']
                ids.append(d['id'])
        return ids
    
def getNearbyRecentMediaById(ids):
    list = []


    for i in ids:
        print i

def getNearbyRecentMediaByLatLon(lat, lng):
    list = []
    r = requests.get(baseUrl + "/media/search?lat=" + lat + "&lng=" + lng + "&access_token=" + access_token)
    if(r.ok):
        ids = []
        data = json.loads(r.text)
        for d in data['data']:
            print 'data'
            if d['type'] == 'video':
                info = {'thumbnail': d['images']['thumbnail']['url'],
                        'location': {'lat': d['location']['latitude'],
                                     'lng': d['location']['longitude']},
                        'videoUrl': d['videos']['low_resolution']['url'],
                        'url': d['link']
                }
                ids.append(info)
        return ids
                     
        
    
@app.route('/', methods=['GET'])
def helloWorld():
    return 'hello'

@app.route('/get/location', methods=['GET'])
def inGet():
    return 'u in get location'

#@app.route('/get/location/search', methods=['GET'])
#def inGetLoc():
#    lat = request.args.get('lat')
#    return 'u searched ' + lat

    
@app.route('/get/location/search', methods=['GET', 'OPTIONS'])
@crossdomains(origin='*')
def getIds():    
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    ids = getNearbyRecentMediaByLatLon(lat, lon)
    response = jsonify(data = ids)
    return response


#    ids = getNearbyLocationIds(lat, lon)
#    idList = []
#    print ids
#    for id in ids:
#        id = {'id': id}
#        idList.append(id)
#        print id
#    return jsonify(data = idList )


    

if __name__ == '__main__':
    app.run(debug=True)
#        app.run(debug=True, host='0.0.0.0')
    



lat = "48"
lon = "2"

ids = getNearbyLocationIds(lat, lon)
print ids

r = requests.get(baseUrl + "/locations/search?lat=48&lng=2&distance=500&access_token=" + access_token)

