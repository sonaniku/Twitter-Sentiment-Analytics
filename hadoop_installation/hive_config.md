# Hive installation with MySql

## Step 1: Download and extract Hive
Download Hive 3.1.2 using this link: 
```
wget https://downloads.apache.org/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz
```
Then extract and move to /usr/local:
```
tar –xvf  apache-hive-3.1.2-bin.tar.gz
mv apache-hive-3.1.2-bin /usr/local/hive
```
Set up environment variables:
```
export HIVE_HOME=/usr/local/hive
export HIVE_CONF=$HIVE_HOME/conf
export HIVE_CONF_DIR=$HIVE_HOME/conf
export PATH=$PATH:$HIVE_HOME/sbin:$HIVE_HOME/bin
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/lib/*:$HIVE_HOME/lib/*
export CLASSPATH=$CLASSPATH:$HIVE_HOME/lib/mysql-connector-java-8.0.26.jar
```
Add to hive-env.sh in config folder:
```
export HADOOP_HOME=/usr/local/hadoop
export HIVE_AUX_JARS_PATH=/usr/local/hive/lib/*
```
Create Hive directories in Hadoop:
```
hdfs dfs -mkdir /tmp
hdfs dfs -chmod g+w /tmp
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod g+w /user/hive/warehouse

```
## Step 1: Install MySql Server
```
sudo apt-get install mysql-server
```
Download mysql-connector-java-8.0.26 on this link:
```
https://jar-download.com/artifacts/mysql/mysql-connector-java/8.0.26/source-code
```
Then move it to Hive lib:
```
mv mysql-connector-java-8.0.26.jar $HIVE_HOME/lib
```