#!/usr/bin/env python3

import jsonpickle
import io
import redis
import hashlib
import os
import platform
import sys
import glob
import time
import pymongo
import json
import pandas as pd



from google.cloud import storage


def read_data(bucket_name, blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("r") as f:
        return pd.read_pickle(f.read())


data = read_data('spotify-million','final_data.pkl')

res_sim = pd.DataFrame(range(len(data.index)), index = data.index,
                                     columns =['sim'])

# Redis
redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379

redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)

# Log
infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())

def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient.lpush('logging', f"{infoKey}:{message}")


from sklearn.metrics.pairwise import cosine_similarity

def find_vector_playlist(playlist):

    return data.loc[playlist].sum(axis = 0)


def calculate_cosine(vector, res_sim):

    res_sim['sim'] = cosine_similarity(data.values, vector.values.reshape(1, -1))[:,0]
    top_15 = res_sim.nlargest(15,'sim')

    return top_15

def delete_duplicates(res,playlist):
    for song in playlist:
        if song in res:
            res.remove(song)
    return res

def process(playlist):

    vector = find_vector_playlist(playlist)
    res = calculate_cosine(vector, res_sim)
    res = list(res.index)
    res = delete_duplicates(res,playlist)

    return res[:10]



log_info('Worker is ready to work!')

while True:
    #try:
    work = redisClient.blpop("toWorker", timeout=0)
    playlist = jsonpickle.decode(work[1])
    username = list(playlist.keys())[0]

    log_info('Songs of '+username+' are received to a worker')

    res = process(playlist[username])
    res = jsonpickle.encode({'playlist':res})

    redisClient.lpush(username,res)
    log_info('Songs of '+username+' are recommended!')

    #except Exception as exp:
    #    print(f"Exception raised in log loop: {str(exp)}")
    sys.stdout.flush()
    sys.stderr.flush()
