import pandas as pd
from collections import Counter
from textblob import TextBlob

def WordFrequency(tweets_filter_df):
    tweets_long_string = tweets_filter_df['tweets_adjectives'].tolist()
    tweets_list=[]
    for item in tweets_long_string:
        item = item.split()
        for i in item:
            tweets_list.append(i)
    counts = Counter(tweets_list)
    df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    df.columns = ['Words', 'Count']
    df = df.sort_values(by='Count', ascending=False )
    return df

# Create function to obtain Subjectivity Score
def getSubjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity

# Create function to obtain Polarity Score
def getPolarity(tweet):
    return TextBlob(tweet).sentiment.polarity

# Create function to obtain Sentiment category
def getSentimentTextBlob(polarity):
    if polarity < 0:
        return "Negative"
    elif polarity == 0:
        return "Neutral"
    else:
        return "Positive"

def TweetSentimentDistribution(tweets_filter_df):
    tweets_filter_df['Subjectivity']=tweets_filter_df['tweets_sentiments'].apply(getSubjectivity)
    tweets_filter_df['Polarity']=tweets_filter_df['tweets_sentiments'].apply(getPolarity)
    tweets_filter_df['Sentiment']=tweets_filter_df['Polarity'].apply(getSentimentTextBlob)
    bar_chart = tweets_filter_df['Sentiment'].value_counts().rename_axis('Sentiment').to_frame('Total Tweets').reset_index()
    return bar_chart