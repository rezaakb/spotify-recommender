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

import pandas as pd

from textblob import TextBlob


working_directory = 'gs://spotify-million/jar-files/mongo-spark-connector-10.0.5.jar'

spark = SparkSession \
    .builder \
    .appName("Spotify") \
    .config("spark.jars", working_directory)\
    .config("spark.mongodb.read.connection.uri", "...")\
    .config("spark.mongodb.write.connection.uri", "...")\
    .getOrCreate()


df_features = spark.read.format("mongodb").option("database","Spotify").option("collection", "music_features").load()

df_features = df_features.drop("type","analysis_url","time_signature")
df_features = df_features.dropDuplicates(['uri'])



casting = F.udf(lambda x : float(x[0]),FloatType())

columns_to_scale = ["danceability", "energy", "loudness", "speechiness","acousticness", "instrumentalness", "liveness", "valence", "tempo"]

for column in columns_to_scale:
    assemblers = VectorAssembler(inputCols=[column], outputCol=column + "_vec")
    scalers = MinMaxScaler(inputCol=column + "_vec", outputCol=column + "_scaled")
    pipeline = Pipeline(stages=[assemblers,scalers])
    scalerModel = pipeline.fit(df_features)
    df_features = scalerModel.transform(df_features)
    df_features = df_features.drop(column)
    df_features = df_features.drop(column+"_vec")
    df_features = df_features.withColumn(column+"_scaled",casting(column+"_scaled"))

print("Normalized!")

encoder = OneHotEncoder(inputCols=['key'], outputCols=['onehot'])
df_features = encoder.fit(df_features).transform(df_features)
df_features = df_features.select('*', vector_to_array('onehot').alias('key_onehot'))
num_categories = len(df_features.first()['key_onehot'])
cols_expanded = [((F.col('key_onehot')[i]*0.5).alias(f'key{i}')) for i in range(num_categories)]
df_features = df_features.select('*', *cols_expanded)
df_features = df_features.drop("onehot","key","key_onehot")


encoder = OneHotEncoder(inputCols=['mode'], outputCols=['onehot'])
df_features = encoder.fit(df_features).transform(df_features)
df_features = df_features.select('*', vector_to_array('onehot').alias('mode_onehot'))
num_categories = len(df_features.first()['mode_onehot'])
cols_expanded = [((F.col('mode_onehot')[i]*0.5).alias(f'mode{i}')) for i in range(num_categories)]


df_features = df_features.select('*', *cols_expanded)
df_features = df_features.drop("onehot","mode","mode_onehot")


df_pro = spark.read.format("mongodb").option("database","Spotify").option("collection", "pro_data").load()
df_pro = df_pro.dropDuplicates(['track_uri'])

df_pro = df_pro.drop("album_uri","artist_uri","duration_ms","pos","name","pid","num_followers","tracks","num_artists")

print("Track URI Fixed")

df_pro = df_pro.join(df_features, df_pro.track_uri == df_features.uri)
df_pro = df_pro.drop(df_features.uri)

df_pro.write.format("mongodb").mode("append").option("database","Spotify").option("collection", "final_data").save()
