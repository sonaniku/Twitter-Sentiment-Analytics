# Tez installation 

## Step 1: Download and extract Tez
Download Tez 0.9.2:
```
wget https://dlcdn.apache.org/tez/0.9.2/apache-tez-0.9.2-bin.tar.gz
```
Extract and move to /usr/local:
```
tar zxf apache-tez-0.9.2-bin.tar.gz
mv apache-tez-0.9.2-bin /usr/local/tez
```
Create the /apps/tez directory on MapR filesystem:
```
hdfs dfs -mkdir /apps
hdfs dfs -mkdir /apps/tez
```
Upload the Tez libraries to the /tez directory on the MapR file system
```
hdfs dfs -put /usr/local/tez /apps/tez
hdfs dfs -put /usr/local/tez/share/tez.tar.gz /apps/tez/tez
hdfs dfs -chmod -R 755 /apps/tez
```
Set the Tez environment variables in file Bashrc
```
export TEZ_CONF_DIR=/usr/local/tez/conf
export TEZ_JARS=/usr/local/tez/*:/usr/local/tez/lib/*
export HADOOP_CLASSPATH=$TEZ_CONF_DIR:$TEZ_JARS:$HADOOP_CLASSPATH
export CLASSPATH=$CLASSPATH:$TEZ_CONF_DIR:$TEZ_JARS:$TEZ_HOME
export TEZ_HOME=/usr/local/tez
export CLASSPATH=$TEZ_CONF_DIR:$TEZ_JARS:$CLASSPATH
```
## Step 2: Configure
Add the following properties to the tez-site.xml file:
```
<property>
  <description>Enable Tez to use the Timeline Server for History Logging</description>
  <name>tez.history.logging.service.class</name>
  <value>org.apache.tez.dag.history.logging.ats.ATSHistoryLoggingService</value>
</property>

<property>
  <description>URL of the location where Tez UI is hosted</description>
  <name>tez.tez-ui.history-url.base</name>
  <value>http://webserver-host:9999/tez-ui/</value>
</property>
```
Download guava-27.0-jre.jar and replace old guava version in /usr/local/tez/lib
```
https://jar-download.com/artifacts/com.google.guava/guava/27.0-jre/source-code
```
Configure Hive for Tez engine in hive-site.xml
```
<property>
  <name>hive.execution.engine</name>
  <value>tez</value>
</property>
```
Change permisson and owner on Tez directory:
```
sudo chown -R h-user:h-user /usr/local/tez
sudo chmod -R 755 /usr/local/tez
```

