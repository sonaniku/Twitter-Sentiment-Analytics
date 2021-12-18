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
Download guava-27.0-jre.jar and replace old guava version in /usr/local/hive/lib
```
https://jar-download.com/artifacts/com.google.guava/guava/27.0-jre/source-code
```
## Step 2: Install MySql Server
```
sudo apt-get install mysql-server
```
Download mysql-connector-java-8.0.26 on this link: (The connector version have to be the same with mysql version)
```
https://jar-download.com/artifacts/mysql/mysql-connector-java/8.0.26/source-code
```
Then move it to Hive lib:
```
cp mysql-connector-java-8.0.26.jar $HIVE_HOME/lib
```
Create username and password:
```
mysql> CREATE USER 'hiveusr'@'%' IDENTIFIED BY 'hivepassword'; 
mysql> GRANT all on *.* to 'hiveuser'@localhost identified by 'hivepassword';
mysql>  flush privileges;
```
## Step 3: Configuring hive-site.xml
```
cd $HIVE_HOME/conf
gedit hive-site.xml
```
Then change value with having folowing <name> tag:
```
<property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://localhost/metastore_db?createDatabaseIfNotExist=true&amp;allowPublicKeyRetrieval=true&amp;useSSL=false</value>
    <description>
      JDBC connect string for a JDBC metastore.
      To use SSL to encrypt/authenticate the connection, provide database-specific SSL flag in the connection URL.
      For example, jdbc:postgresql://myhost/db?ssl=true for postgres database.
    </description>
</property>

<property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.cj.jdbc.Driver</value>
    <description>MySQL JDBC driver class</description>
</property>

<property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hiveusr</value>
    <description>Username to use against metastore database</description>
</property>

<property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>hivepassword</value>
    <description>password to use against metastore database</description>
</property>

<property>
    <name>hive.server2.thrift.port</name>
    <value>10010</value>
    <description>Port number of HiveServer2 Thrift interface when hive.server2.transport.mode is 'binary'.</description>
</property>

<property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
    <description>
      Setting this property to true will have HiveServer2 execute
      Hive operations as the user making the calls to it.
    </description>
</property>
```
Initialize Hive metastore on MySql:
```
schematool -initSchema -dbType mysql
```
Change permisson and owner on Hive directory:
```
sudo chown -R h-user:h-user /usr/local/hive
sudo chmod -R 755 /usr/local/hive
```
