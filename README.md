# You need to install this

Python 
- 3.10.0

Django 
- 3.2.10

# Required packages:
- pip install djangorestframework
-  pip install https://download.lfd.uci.edu/pythonlibs/w6tyco5e/sasl-0.3.1-cp310-cp310-win_amd64.whl
- pip install requests
- pip install requests_oauthlib
- pip install pandas
- pip install textblob
- pip install pyorc
- pip install pycountry_convert
- pip install emot
- pip install nltk
- pip install tweepy
- pip install numpy
- pip install hdfs
- pip install pyhive
- pip install thrift-sasl
- pip install thrift

# Hit to run server:
## Start Hadoop server 
Execute these command on Hadoop primary machine, wait a minute for them to become stable
```
start-dfs.sh
start-yarn.sh
mapred --daemon start historyserver
hiveserver2
```
## Start Django web application
Add your own credentials in settings.py, then run the application
- python manage.py runserver