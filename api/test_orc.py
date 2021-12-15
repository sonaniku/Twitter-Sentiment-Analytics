import pyorc
import os 
print("-----------------TWEETS ORC--------------")
tweets_orc = "F:\\Twitter-Cloud-Project\\Twitter Sentiment Analytics\\main\\api\\tmp_search_tweets_orc\\77"
with open(tweets_orc, "rb") as data:
        print(data)
        reader = pyorc.Reader(data)
        print(len(reader))
        print(reader.schema)
        for row in reader:  
            print(row)
print("-----------------TWEETS ORC--------------")
import pyorc
#with open(".\\tmp_search_tweets_orc\\63", "r") as data:
#    data.read()