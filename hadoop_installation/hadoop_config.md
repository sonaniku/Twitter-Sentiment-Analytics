# Prerequisites

Oracle VirtualBox download link:
https://www.virtualbox.org/wiki/Downloads

Ubuntu Server 20.04 ISO download link: (recommended storage: 30GB)
https://releases.ubuntu.com/20.04/

Install Ubuntu on a virtual box tutorial: 
https://brb.nci.nih.gov/seqtools/installUbuntu.html

# Hadoop installation

## Step 1: Install ssh & psdh
First set up virtual box network to bridge network
Then install:
```
sudo apt install ssh
sudo apt install pdsh
```
Set pdsh environment to ssh
Add to the end of Bashrc file:
```
export PDSH_RCMD_TYPE=ssh
```
## Step 2: Generate a SSH key
Generate a ssh key with the following command:
```
ssh-keygen -t rsa -P ""
```
Then clone the key into authorized_keys files:
```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

## Step 3: Install Java 8
Using openjdk:
```
sudo apt install openjdk-8-jdk
```
Set up Java_Home environment:
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
```

## Step 4: Download and install hadoop
Download:
```
sudo wget -P ~ https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
```
When the download is finish unzip it:
```
tar xzf hadoop-3.3.1.tar.gz
mv hadoop-3.3.1 hadoop
```
Configure the Java path on Hadoop’s virtual environment:
```
sudo nano ~/hadoop/etc/hadoop/hadoop-env.sh
```
Then look for Java_Home’s line and replace it by:
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
```
Move the hadoop directory to our user local file:
```
sudo mv hadoop /usr/local/hadoop
```
Set up hadoop path:
```
sudo nano /etc/environment
```
Add
```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/hadoop/bin:/usr/local/hadoop/sbin"
JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/jre"
```
## Step 5: Create a specific user for Hadoop
```
sudo adduser h-user
sudo usermod -aG hadoopuser h-user
sudo chown h-user:root -R /usr/local/hadoop/
sudo chmod g+rwx -R /usr/local/hadoop/
sudo adduser h-user sudo
```
## Step 6: Clone the primary machine in order to create another secondary machine
>Choose full clone with different MAC Address.

## Step 7: Change hostnames
```
sudo nano /etc/hostname
```
Add the name you want, example:
-Primary machine: h-primary
-Secondary machine: h-secondary
Then reboot all machines.
After that, add other machine's IP and hostname in hosts file on both machines:
```
sudo nano /etc/hosts
```
## Step 8: Set up ssh on Primary with our user
Generate a ssh key for this user:
```
su - h-user
ssh-keygen -t rsa
```
Copy the ssh key to secondary machine:
```
ssh-copy-id h-user@h-primary
ssh-copy-id h-user@h-secondary
```
## Step 9: Configure Hadoop Service Port
Change hadoop port configurations: (only on primary)
```
sudo nano /usr/local/hadoop/etc/hadoop/core-site.xml
```
And then add to file’s configuration:
```
<property>
<name>fs.defaultFS</name>
<value>hdfs://h-primary:9000</value>
</property>
```
## Step 10: Configuration of HDFS system
Change HDFS configurations: (only on primary)
```
sudo nano /usr/local/hadoop/etc/hadoop/hdfs-site.xml
```
And then add to file’s configuration:
```
    <property>
		<name>dfs.namenode.name.dir</name>
		<value>/usr/local/hadoop/data/nameNode</value>
	</property>
	<property>
		<name>dfs.datanode.data.dir</name>
		<value>/usr/local/hadoop/data/dataNode</value>
	</property>
	<property>
		<name>dfs.replication</name>
		<value>2</value>
	</property>
	<property>
		<name>dfs.namenode.http-address</name>
		<value>0.0.0.0:10000</value>
	</property>
	<property>
    		<name>dfs.client.datanode-restart.timeout</name>
    		<value>30</value>
	</property>
	<property> 
	    	<name>dfs.webhdfs.enabled</name> 
	    	<value>true</value> 
	</property> 
```
Change mapred-site.xml configuration: (only on primary)
```
    <property>
		<name>mapreduce.framework.name</name>
		<value>yarn-tez</value>
	</property>
	 <property>
		<name>yarn.app.mapreduce.am.env</name>
		<value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
	</property>
	<property>
		<name>mapreduce.map.env</name>
		<value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
	</property>
	<property>
		<name>mapreduce.reduce.env</name>
		<value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
	</property>
	<property>
		<name>mapreduce.jobhistory.address </name>
		<value>dat-master:10020</value>
	</property>
	<property>
		<name>mapreduce.jobhistory.webapp.address</name>
		<value>dat-master:19888</value> 
	</property>
```
Change yarn-site.xml configuration: (only on primary)
```
    <property>
		<name>yarn.resourcemanager.hostname</name>
		<value>dat-master</value>
	</property>
	<property>
        <name>yarn.log.server.url</name>
       	<value>http://dat-master:19888/jobhistory/logs</value>
	</property>
    <property>
	 	<name>hive_timeline_logging_enabled</name>
	 	<value>true</value>
	 </property>
	 <property>
	 	<name>yarn.acl.enable</name>
	 	<value>false</value>
	 </property>
	 <property>
	  <name>yarn.nodemanager.aux-services</name>
	  <value>tez_shuffle</value>
	</property>
	<property>
	  <name>yarn.nodemanager.aux-services.tez_shuffle.class</name>
	  <value>org.apache.tez.auxservices.ShuffleHandler</value>
	</property>
	<property>
 		<name>yarn.log-aggregation-enable</name>
 		<value>true</value>
	</property>
	<property>
	  <description>Indicate to clients whether Timeline service is enabled or not.
	  If enabled, the TimelineClient library used by end-users will post entities
	  and events to the Timeline server.</description>
	  <name>yarn.timeline-service.enabled</name>
	  <value>false</value>
	</property>	
	<property>
	  <description>The hostname of the Timeline service web application.</description>
	  <name>yarn.timeline-service.hostname</name>
	  <value>h-primary</value>
	</property>
	<property>
	  <description>Enables cross-origin support (CORS) for web services where
	  cross-origin web response headers are needed. For example, javascript making
	  a web services request to the timeline server.</description>
	  <name>yarn.timeline-service.http-cross-origin.enabled</name>
	  <value>true</value>
	</property>
	<property>
	  <description>Publish YARN information to Timeline Server</description>
	  <name> yarn.resourcemanager.system-metrics-publisher.enabled</name>
	  <value>true</value>
	</property>
```
Identify the workers - 
Add the secondary machines name (h-secondary) to workers file: (only on primary)
```
sudo nano /usr/local/hadoop/etc/hadoop/workers
```
Finally copy configurations into secondary machines:
```
scp /usr/local/hadoop/etc/hadoop/* h-secondary:/usr/local/hadoop/etc/hadoop/
```
## Step 11: Formatting and Starting HDFS system (only primary)
Start for making sure that all changes are applied:
```
source /etc/environment
source ~/.bashrc
```
Then format the hdfs system with:
```
hdfs namenode -format
```
## Step 12: Yarn configuration
To set up yarn you need to start for exporting all paths: (on primary)
```
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_MAPRED_HOME=${HADOOP_HOME} 
export HADOOP_COMMON_HOME=${HADOOP_HOME}
export HADOOP_HDFS_HOME=${HADOOP_HOME} 
export YARN_HOME=${HADOOP_HOME}
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native 
export PATH=$PATH:$HADOOP_HOME/sbin
export PATH=$PATH:$HADOOP_HOME/bin
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$TEZ_HOME/*:$TEZ_HOME/lib/*
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:/usr/local/hive/lib/* 
export LIB_JARS=/usr/local/hive/lib/*
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-client-common-3.3.1.jar
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-client-shuffle-3.3.1.jar
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.3.1.jar
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/common/hadoop-common-3.3.1.jar
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/common/hadoop-common-3.3.1-tests.jar
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/common/lib/*
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/mapreduce2/*
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/yarn/*
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/mapreduce/*
export CLASSPATH=$CLASSPATH:$HADOOP_HOME/share/hadoop/common/*
```
Now just change yarn’s configuration on the secondary:
```
sudo nano /usr/local/hadoop/etc/hadoop/yarn-site.xml
```
And then add the following configurations:
```
<property>
<name>yarn.resourcemanager.hostname</name>
<value>h-primary</value>
</property>
```
