from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import QueryListSerializer
from .models import Query_Archived

from . import search_tweets
from . import hive_connection
from .tweets_exploration import WordFrequency, TweetSentimentDistribution
import pandas as pd

import json
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Query_List':'/query-list/',
        'Create_Query':'/query-create/',
        'Filter':'/query-filter/<str:pk>',
    }
    return Response(api_urls)

@api_view(['POST'])
def Query_Add(request): #and search tweets
    serializer = QueryListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    orc_file_id = serializer.data["id"]
    query_string = serializer.data["query_string"]
    geo = serializer.data["geo"]
    encoded_query = query_string.encode('utf-8')
    
    # search_tweets and save to .orc
    try: 
        search_tweets.tweets_mining(query_string, geo, orc_file_id)
    except Exception as ex:
        print(ex)
    #
    return Response(serializer.data)


@api_view(['GET'])
def Dashboard_Filter(request, query_id, date_created_at): #get data from Hive
    a=b=c=d=e=""
    result = hive_connection.FilterFromHive(query_id, date_created_at)
    print(result)
    if(len(result)):
        tweets_filter_df=pd.DataFrame(result, columns=["tweet_id", "hour_created_at", "retweet", "favorite", "tweets_adjectives", "tweets_sentiments", "date_created_at" ])
        word_frequency = WordFrequency(tweets_filter_df).head(10)
        tweet_sentiment_distribution = TweetSentimentDistribution(tweets_filter_df)
        
        time_series_of_tweets = tweets_filter_df.groupby('hour_created_at').size().reset_index(name='counts')
        time_series_of_tweets = time_series_of_tweets.sort_values(by='hour_created_at', ascending=True)

        most_retweet_tweets = tweets_filter_df.sort_values(by="retweet", ascending=False).head(10)

        most_liked_tweets = tweets_filter_df.sort_values(by="favorite", ascending=False).head(10)

        most_retweet_tweets = most_retweet_tweets[["tweet_id", "retweet"]]
        most_liked_tweets = most_liked_tweets[["tweet_id", "favorite"]]

        a = json.loads(word_frequency.to_json(orient="records"))
        b = json.loads(tweet_sentiment_distribution.to_json(orient="records"))
        c = json.loads(time_series_of_tweets.to_json(orient="records"))
        d = json.loads(most_retweet_tweets.to_json(orient="records"))
        e = json.loads(most_liked_tweets.to_json(orient="records"))

    return JsonResponse({"Word_Frequency":a, "Sentiment_Count":b, "Time_Series":c, "Top_10_retweeted": d, "Top_10_liked": e}, safe=False)

@api_view(['GET'])
def Query_List(request): #get list from Query_Archived for dropdown menu
    query_list = Query_Archived.objects.all()
    serializer = QueryListSerializer(query_list, many=True)
    return Response(serializer.data)

