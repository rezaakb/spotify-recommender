from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import col, count, countDistinct, explode, udf
from pyspark.ml import Pipeline
from pyspark.ml.feature import MinMaxScaler, VectorAssembler, OneHotEncoder, HashingTF, IDF, Tokenizer, CountVectorizer
from pyspark.ml.functions import vector_to_array


import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from google.cloud import storage

import pandas as pd

from textblob import TextBlob

#key_path = "/home/r_akbarian2009/key.json"

working_directory = 'gs://spotify-million/jar-files/mongo-spark-connector-10.0.5.jar'

spark = SparkSession \
    .builder \
    .appName("Spotify") \
    .config("spark.jars", working_directory)\
    .config("spark.mongodb.write.connection.uri", "...")\
    .getOrCreate()


playlist_file = 'gs://spotify-million/spotify_million_playlist_dataset/data'

play_df = spark.read.option("multiline", "true").json(playlist_file)


df = play_df.select('playlists', explode('playlists')).\
                    select(explode('col.tracks'),'col.name','col.pid',
                       'col.num_followers', 'col.num_tracks','col.duration_ms','col.num_artists').\
                        withColumnRenamed('col.num_followers', 'num_followers').\
                        withColumnRenamed('col.num_tracks', 'tracks').\
                        withColumnRenamed('col.duration_ms', 'duration_ms').\
                        withColumnRenamed('col.num_artists', 'num_artists').\
                        withColumnRenamed('col.pid', 'pid').\
                        withColumnRenamed('col.name', 'name').\
                        select('col.*','*').drop('col')


def SentimentAnalysis(text):
    '''
    Getting the Subjectivity and Polarity using TextBlob
    '''
    res = [0,0,0,0,0,0]

    score = TextBlob(text).sentiment.subjectivity

    if score < 1/3:
        res[0] = 0.3
    elif score > 1/3:
        res[2] = 0.3
    else:
        res[1] = 0.3

    score = TextBlob(text).sentiment.polarity
    if score < 0:
        res[3] = 0.5
    elif score == 0:
        res[4] = 0.5
    else:
        res[5] = 0.5

    return tuple(res)

schema = StructType([
    StructField("sub|low", FloatType(), False),
    StructField("sub|meduim", FloatType(), False),
    StructField("sub|high", FloatType(), False),
    StructField("pol|neg", FloatType(), False),
    StructField("pol|nat", FloatType(), False),
    StructField("pol|pos", FloatType(), False),
])

SentimentAnalysis_udf = udf(SentimentAnalysis, schema)

tmp = df.select("track_name").distinct()
tmp = tmp.withColumn('extracted', SentimentAnalysis_udf('track_name')).select(col("track_name"),col("extracted.*"))

df = df.join(tmp, df.track_name == tmp.track_name)
df = df.drop(tmp.track_name)

df.write.format("mongodb").mode("append").option("database","Spotify").option("collection", "pro_data").save()
