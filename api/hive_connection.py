## HDFS ##
from hdfs import InsecureClient
from pyhive.hive import Cursor

hdfsclient = InsecureClient('http://192.168.1.110:10000', user='h-user')

## HIVE ##
from pyhive import hive
import json
host_name = "192.168.1.110"
port = 10010
user = "scott"
password = "tiger"
database="twitter_sentiment"
hdfs_tmp_dir = "/tweets_tmp"
def HiveConnection(host_name, port, user,password, database):
    try:
        conn = hive.Connection(host=host_name, port=port, username=user, password=password,
                        database=database, auth='CUSTOM')
        return conn
    except Exception as ex:
        print(ex)
    
def UploadToHive(tweets_orc_local, id):
    conn = HiveConnection(host_name, port, user, password, database)
    cur = conn.cursor()
    hdfs_file_path = hdfs_tmp_dir + "/" + str(id)
    hdfsclient.upload(hdfs_file_path, tweets_orc_local) # upload local_tmp_orc to hdfs_tmp_orc
    try:
        print("CREATE TABLE tweet_"+ str(id) + " (tweet_id STRING, hour_created_at STRING, \
            retweet INT, favorite INT, tweets_adjectives STRING, tweets_sentiments STRING) PARTITIONED BY(date_created_at STRING) STORED AS ORC")
        cur.execute("CREATE TABLE tweet_"+ str(id) + " (tweet_id STRING, hour_created_at STRING, \
            retweet INT, favorite INT, tweets_adjectives STRING, tweets_sentiments STRING) PARTITIONED BY(date_created_at STRING) STORED AS ORC")
    except Exception as ex: print(ex)
    try:
        print("LOAD DATA INPATH \'"+ hdfs_file_path +"\' INTO TABLE tweet_" + str(id))
        cur.execute("LOAD DATA INPATH \'"+ hdfs_file_path +"\' INTO TABLE tweet_" + str(id))
    except Exception as ex: print(ex)
    conn.close()

def FilterFromHive(query_id, date_created_at):
    result = {}
    tweet_table_name = "tweet_" + query_id
    conn = HiveConnection(host_name, port, user, password, database)
    cur = conn.cursor()
    if(date_created_at != "All"):
        cur.execute("SELECT * FROM "+ tweet_table_name +" WHERE date_created_at=\'"+date_created_at+"\'")
    else:
        cur.execute("SELECT * FROM "+ tweet_table_name)
    result = cur.fetchall()
    conn.close()
    return result


