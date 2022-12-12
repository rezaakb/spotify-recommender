#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response, render_template
import jsonpickle
from PIL import Image
import base64
import io
import redis
import pymongo
import json
import platform
import os
import random
import sys


config_file = json.load(open('../config.json'))

client = pymongo.MongoClient(config_file["mongo_str"])

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=config_file["spotify_client_id"], client_secret=config_file["spotify_client_secret"])
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


#db = client["Spotify"]
#songs_info = db["songs_info"]
#list_all_songs = list(songs_info.find())


# Initialize the Flask application
app = Flask(__name__)


# Logging
infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())

def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

# Redis
redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379
redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)





@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/search_songs', methods=['GET','POST'])
def search_songs():

    query = request.get_json()
    query = query['query']

    if len(query)>2:
        db = client["Spotify"]
        collection = db["songs_info"]
        query_dict = {"$or":[{
                            "artist_name": {
                            "$regex": query,
                            "$options" :'i'
                            }
                            },{
                            "track_name": {
                            "$regex": query,
                            "$options" :'i'
                            }
                    }]}

        mydoc = list(collection.find(query_dict, { 'track_name': 1, 'artist_name': 1,  'id':1, '_id':0 }))
        mydoc = mydoc[:min(20, len(mydoc))]
    else:
        mydoc = []
    print(mydoc)
    response = {'list' : mydoc}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/send_playlist', methods=['POST'])
def send_playlist():
    data = request.get_json()
    username = str(random.getrandbits(128))


    list_songs = []
    for i in range(len(data['data'])):
        if data['data'][i]!=-1:
            list_songs.append(data['data'][i])

    redis_songs = jsonpickle.encode({username:list_songs})

    # Add to redis
    redisClient.lpush('toWorker', redis_songs)
    log_info('Songs of '+username+' added to Redis')


    results = redisClient.blpop(username, timeout=0)
    log_info('Recommended songs of '+username+' are ready to show.')

    results = jsonpickle.decode(results[1])

    list_songs = results['playlist']
    res = []

    for song_id in list_songs:

        db = client["Spotify"]
        collection = db["songs_info"]

        tmp = collection.find_one({"id" :song_id} , { 'track_name': 1, 'artist_name': 1,  'id':1, '_id':1 })
        tmp["url"] = 'https://open.spotify.com/track/'+song_id

        img_track = sp.track(song_id)
        tmp["img_url"] = img_track['album']['images'][-1]['url']

        res.append(tmp)


    redis_songs = jsonpickle.encode({'final' : res})
    print(redis_songs)
    # Recive from redis

    return Response(response=redis_songs, status=200,  mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=8000, debug=False)
