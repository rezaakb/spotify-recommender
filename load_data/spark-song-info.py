from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import col, count, countDistinct, explode, udf
from pyspark.ml import Pipeline
from pyspark.ml.feature import MinMaxScaler, VectorAssembler, OneHotEncoder, HashingTF, IDF, Tokenizer, CountVectorizer
from pyspark.ml.functions import vector_to_array
import time

import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from google.cloud import storage

working_directory = 'gs://spotify-million/jar-files/mongo-spark-connector-10.0.5.jar'

spark = SparkSession \
    .builder \
    .appName("Spotify") \
    .config("spark.jars", working_directory)\
    .config("spark.mongodb.read.connection.uri", "...")\
    .config("spark.mongodb.write.connection.uri", "...")\
    .getOrCreate()


df = spark.read.format("mongodb").option("database","Spotify").option("collection", "final_data").load()


tmp = df.select("id","track_name","artist_name")
tmp.write.format("mongodb").mode("append").option("database","Spotify").option("collection", "songs_info").save()
