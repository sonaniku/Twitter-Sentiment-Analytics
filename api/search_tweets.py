# to make more than one plot in Plotly
from main.settings import ORC_TMP_FOLDER
from datetime import date

from main.settings import ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET, BEARER_TOKEN
import pycountry_convert as pc
import os
from emot.emo_unicode import UNICODE_EMOJI, EMOTICONS_EMO  # For emojis
from collections import Counter

# TextBlob - Python library for processing textual data
from textblob import TextBlob
from nltk import pos_tag  # For Parts of Speech tagging
from nltk.stem import WordNetLemmatizer  # to reduce words to orginal form
from nltk.tokenize import word_tokenize  # to create word tokens
# get stopwords from NLTK library & get all words in english language

from nltk.corpus import stopwords, words
import nltk
import tweepy  # for tweet mining
import pandas as pd  # for data manipulation and analysis
import numpy as np
# for working with arrays and carrying out mathematical operations. Pandas is built on Numpy
import numpy as np
import pyorc
import csv  # to read and write csv files
import re  # In-built regular expressions library
import string  # Inbuilt string library
import requests  # to send HTTP requests

import math
# Set the limits for Pandas Dataframe display to avoid potential system freeze
pd.set_option("display.max_rows", 15)
pd.set_option("display.max_columns", 15)
pd.set_option('display.max_colwidth', 40)

from . import hive_connection

client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_KEY,
                       access_token_secret=ACCESS_SECRET,
                       wait_on_rate_limit=True)


"""def get_tweets_orc_geo(query, tweets_orc,
                            limit=20,
                            tweet_fields=['id', 'created_at',
                                          'text', 'public_metrics'],
                            user_fields=['location'],
                            place_fields=['country_code'],
                            expansions=['geo.place_id', 'author_id'],
                            max_results=10):

    pages = tweepy.Paginator(client.search_recent_tweets, query=query,
                             tweet_fields=tweet_fields,
                             place_fields=place_fields,
                             user_fields=user_fields,
                             expansions=expansions,
                             max_results=max_results,
                             limit=limit)

    # i = 0
    tweets_df = pd.DataFrame(columns=['tweet_id', 'date_created_at', 'hour_created_at', 'text', 
    'user_location' , 'retweet', 'favorite'])
    count=0
    try:
        for list_tweets in pages:
            # if i == 0:
                # i = 1
                # print(list_tweets)
            for tweet in list_tweets.data:
                tweet_id = str(tweet.id)
                created_at = tweet.created_at
                date_created_at = str(tweet.created_at).split(" ")[0]
                hour_created_at = str(
                    str(tweet.created_at).split(" ")[1]).split(":")[0]

                text = tweet.text
                key_user = "users"
                users = {u["id"]: u for u in list_tweets.includes[key_user]}
                if users[tweet.author_id]:
                    u = users[tweet.author_id]
                    if u.location:
                        user_location = u.location
                    else:
                        user_location = "No location"

                retweet = tweet.public_metrics["retweet_count"]
                favorite = tweet.public_metrics["like_count"]

                key_places = "places"
                places = {}
                if key_places in list_tweets.includes:
                    places = {
                        p["id"]: p for p in list_tweets.includes[key_places]}
                country_code = "No location"
                if tweet.geo is not None:
                    place = places[tweet.geo["place_id"]]
                    country_code = place.country_code
                tweets_df = tweets_df.append({'tweet_id':tweet_id, 'date_created_at':date_created_at,
                'hour_created_at':hour_created_at, 'text':text, 'user_location':user_location, 
                'retweet':retweet, 'favorite':favorite}, ignore_index=True)
                    # csv_writer.writerow([tweet_id, created_at, date_created_at, hour_created_at, text,
                    #                   user_location, retweet, favorite])  # write each row
                count+=1
        print("COUNT = " + str(count))
        return tweets_df
    except Exception as ex:
        print(ex)"""


def get_tweets(query, tweets_orc,
                        limit=20,
                        tweet_fields=['id', 'created_at',
                                      'text', 'public_metrics'],
                        expansions=['author_id'],
                        max_results=10):

    pages = tweepy.Paginator(client.search_recent_tweets, query=query,
                             tweet_fields=tweet_fields,
                             expansions=expansions,
                             max_results=max_results,
                             limit=limit)
    # i = 0
    tweets_df = pd.DataFrame(columns=['tweet_id', 'date_created_at', 'hour_created_at', 'text', 
     'retweet', 'favorite'])
    try:
        for list_tweets in pages:
            # if i == 0:
            # print(list_tweets)
            # i = 1
            for tweet in list_tweets.data:
                tweet_id = tweet.id
                created_at = tweet.created_at
                date_created_at = str(tweet.created_at).split(" ")[0]
                hour_created_at = str(
                    str(tweet.created_at).split(" ")[1]).split(":")[0]
                text = tweet.text
                retweet = tweet.public_metrics["retweet_count"]
                favorite = tweet.public_metrics["like_count"]

                key_places = "places"
                places = {}
                if key_places in list_tweets.includes:
                    places = {
                        p["id"]: p for p in list_tweets.includes[key_places]}
                country_code = "No location"
                if tweet.geo is not None:
                    place = places[tweet.geo["place_id"]]
                    country_code = place.country_code
                tweets_df = tweets_df.append({'tweet_id':tweet_id, 'date_created_at':date_created_at,
                'hour_created_at':hour_created_at, 'text':text, 
                'retweet':retweet, 'favorite':favorite}, ignore_index=True)
                    # create an instance of csv object
                    # csv_writer.writerow([tweet_id, created_at, date_created_at, hour_created_at, text,
                    #                    country_code, retweet, favorite])  # write each row
        return tweets_df
    except Exception as ex:
        print(ex)


def load_orc_to_df(tweets_orc):
    tweets = []

    # Convert each csv to a dataframe
    # df = pd.read_orc(tweets_orc, index_col=None, header=0)
    # tweets.append(df)
    print("-----------------TWEETS ORC--------------")
    with open(tweets_orc, "rb") as data:
        reader = pyorc.Reader(data)
        for row in reader:
            print(row)
    print("-----------------TWEETS ORC--------------")

    # Merge all dataframes
    # tweets_df = pd.concat(tweets, axis=0, ignore_index=True)

    # return tweets_df



def data_cleaning(tweets_df):
    #tweets_df.shape  # Get number of rows and columns
    tweets_df.duplicated(subset='tweet_id').sum()  # Check for duplicate values
    tweets_df = tweets_df.drop_duplicates(
        subset=['tweet_id'])  # drop duplicate values
    #tweets_df.shape  # Check the shape after dropping duplicates
    #tweets_df.isna().any()  # Check for "NaN" values


"""def getContinent(country_code):
    continent_name = "No location"
    if country_code != "No location":
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = pc.convert_continent_code_to_continent_name(
            continent_code)
    return continent_name"""


stop_words = list(stopwords.words('english')) + list(string.ascii_lowercase)
emojis = list(UNICODE_EMOJI.keys())  # full list of emojis
word_list = words.words()  # all words in English language


def preprocessTweets(tweet):
    tweet = tweet.lower()  # has to be in place
    # Remove urls
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    # Remove user @ references and '#' from tweet
    tweet = re.sub(r'\@\w+|\#|\d+', '', tweet)
    # Remove stopwords
    tweet_tokens = word_tokenize(tweet)  # convert string to tokens
    filtered_words = [w for w in tweet_tokens if w not in stop_words]
    filtered_words = [w for w in filtered_words if w not in emojis]
    filtered_words = [w for w in filtered_words if w in word_list]

    # Remove punctuations
    unpunctuated_words = [
        char for char in filtered_words if char not in string.punctuation]
    unpunctuated_words = ' '.join(unpunctuated_words)

    # join words with a space in between them
    return "".join(unpunctuated_words)


def getAdjectives(tweet):
    tweet = word_tokenize(tweet)  # convert string to tokens
    tweet = [word for (word, tag) in pos_tag(tweet)  # part-of-speech-tag ## tag=="JJ" mean that word is an adjectives
             if tag == "JJ"]  # pos_tag module in NLTK library
    return " ".join(tweet)  # join words with a space in between them

# function to return words to their base form using Lemmatizer


def preprocessTweetsSentiments(tweet):
    tweet_tokens = word_tokenize(tweet)
    lemmatizer = WordNetLemmatizer()  # instatiate an object WordNetLemmatizer Class
    lemma_words = [lemmatizer.lemmatize(w) for w in tweet_tokens]
    return " ".join(lemma_words)


"""URL = "https://geocode.search.hereapi.com/v1/geocode"  # Deevloper Here API link
# Acquire api key from developer.here.com
api_key = '-b03lC2YtoHJCFT1SpAAC6hLjc5QrqvxFWPj71jXBkk'


def getCoordinates(location):
    try:
        PARAMS = {'apikey': api_key, 'q': location}  # required parameters
        r = requests.get(url=URL, params=PARAMS)  # pass in required parameters
        # get raw json file. I did  this because when I combined this step with my "getLocation" function,
        # it gave me error for countries with no country_code or country_name. Hence, I needed to use try - except block
        data = r.json()  # Raw json file
    except Exception as ex:
        print(ex)
    return data"""


"""def getLocation(location):
    for data in location:
        if len(location['items']) > 0:
            latitude = location['items'][0]['position']['lat']
            longitude = location['items'][0]['position']['lng']
            try:
                country_code = location['items'][0]['address']['countryCode']
                country_code = pc.country_alpha3_to_country_alpha2(
                    country_code)
                country_name = location['items'][0]['address']['countryName']
            except KeyError:
                country_code = float('Nan')
                country_name = float('Nan')
        else:
            latitude = float('Nan')
            longitude = float('Nan')
            country_code = "No location"
            country_name = float('Nan')
        result = (latitude, longitude, country_code, country_name)
    return result"""

"""def load_df_to_orc_geo(tweets_df, tweets_orc):
    print("------------TWEETS DF---------")
    print(tweets_df)
    print("------------TWEETS DF---------")
    with open(tweets_orc, 'wb') as data:
        for index, row in tweets_df.iterrows():
            print(row["tweet_id"])
            print(type(row["tweet_id"]))
            print(row["date_created_at"])
            print(type(row["date_created_at"]))
            print(row["hour_created_at"])
            print(type(row["hour_created_at"]))
            print(row["text"])
            print(type(row["text"]))
            print(row["user_location"])
            print(type(row["user_location"]))
            print(row["retweet"])
            print(type(row["retweet"]))
            print(row["favorite"])
            print(type(row["favorite"]))
            with pyorc.Writer(data, "struct<c0:string,c1:string,c2:string,c3:string,c4:string,c5:string,c6:string>") as writer:
                writer.write((str(row['tweet_id']), str(row['date_created_at']), str(row['hour_created_at']), 
                str(row['text']), str(row['user_location']), str(row['retweet']), str(row['favorite'])))
    data.close()"""
    

def load_df_to__tmp_orc(tweets_df, tweets_orc):
    with open(tweets_orc, 'wb') as data:
        with pyorc.Writer(data, "struct<tweet_id:string,date_created_at:string,hour_created_at:string,retweet:int,favorite:int,tweets_adjectives:string,tweets_sentiments:string>") as writer:
            for index, row in tweets_df.iterrows():
                tweet_id = row["tweet_id"]
                date_created_at = row['date_created_at']
                hour_created_at = row['hour_created_at']
                retweet = row['retweet']
                favorite = row['favorite']
                tweets_adjectives = row['Tweets_Adjectives']
                tweets_sentiments = row['Tweets_Sentiments']
                tuple = (str(tweet_id), date_created_at, hour_created_at, 
                    retweet, favorite, tweets_adjectives, tweets_sentiments)
                writer.write(
                    tuple
                )
    data.close()

def tweets_mining(query, geo, orc_file_id):
    tweets_orc = os.path.join(ORC_TMP_FOLDER, str(orc_file_id))
    if(geo == True):
        pass
    else:
        tweets_df = get_tweets(query, limit=5, tweets_orc=tweets_orc)
    
    print(tweets_df.head())

    data_cleaning(tweets_df)
    
    # print(tweets_df.head())

    tweets_df['Processed_Tweets'] = tweets_df['text'].apply(preprocessTweets)
    tweets_df['Tweets_Adjectives'] = tweets_df['Processed_Tweets'].apply(
        getAdjectives)
    # print(tweets_df.head())  # Check dataframe first 5 rows)

    tweets_df['Tweets_Sentiments'] = tweets_df['Processed_Tweets'].apply(
        preprocessTweetsSentiments)
    tweets_df.drop(["Processed_Tweets", 'text'], axis=1, inplace=True)
    print(tweets_df.head())
    load_df_to__tmp_orc(tweets_df, tweets_orc)
    hive_connection.UploadToHive(tweets_orc, orc_file_id)

"""def tweets_filter(query_id, date_created, continent, country, geo, path_csv):
    tweets_filter_csv = os.path.join(path_csv, "preprocessed_tweets.csv")
    tweets_df = load_csv_to_df(tweets_filter_csv)
    if(geo == "True"):
        filtered_tweets_df = []
        if continent != "All" & country != "All":
            filtered_tweets_df = tweets_df[(tweets_df["date_created_at"] == date_created)
                                       & (tweets_df["Continent_Name"] == continent) & 
                                       (tweets_df["Country_Code"] == country)]
        elif continent != "All" & country =="All":
            filtered_tweets_df = tweets_df[(tweets_df["date_created_at"] == date_created)
                                       & (tweets_df["Continent_Name"] == continent)]
        elif continent == "All" & country != "All":
            filtered_tweets_df = tweets_df[(tweets_df["date_created_at"] == date_created)
                                       & (tweets_df["Country_Code"] == country)]
        else: filtered_tweets_df = tweets_df[(tweets_df["date_created_at"] == date_created)]

        return filtered_tweets_df
    else:
        filtered_tweets_df = []
        filtered_tweets_df = tweets_df[(
            tweets_df["date_created_at"] == date_created)]
        return filtered_tweets_df


def word_count_df(tweets_adjectives):
    word_count_df_result = []
    tweets_long_string = tweets_adjectives.tolist()
    tweets_list = []
    # print(type(tweets_long_string))
    for item in tweets_long_string:
        # print(type(item))
        # print(item)
        if type(item) is not float :
            item = item.split()
            for i in item:
                tweets_list.append(i)
    # print(tweets_list)
    counts = Counter(tweets_list)
    # print(counts)
    word_count_df_result = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    word_count_df_result.columns = ['Words', 'Count']
    word_count_df_result.sort_values(by='Count', ascending=False, inplace=True)
    return word_count_df_result"""