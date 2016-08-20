#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
from flask import Flask, request, jsonify

access_token = '1555940494.e029fea.f4f3539e108d4079b960d11199a97a9f'
client_secret = '715faafee65a4a7eb498c216adc72771'

baseUrl = "https://api.instagram.com/v1"

app = Flask(__name__)

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
                        'location': {'lat': lat,
                                     'lng': lng},
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

    
@app.route('/get/location/search', methods=['GET'])
def getIds():
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    ids = getNearbyRecentMediaByLatLon(lat, lon)
    return jsonify(data = ids)


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

