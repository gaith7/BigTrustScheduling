#!/bin/bash

echo "remove old Hadoop installation files"
#sudo cp -a /usr/local/hadoop/. /usr/local/hadoop_prev
sudo rm -r /usr/local/hadoop
sudo mkdir /usr/local/hadoop
sudo chmod 777 -R /usr/local/hadoop

echo "Download newest render"
wget 192.168.56.1/hadoop-2.6.0.tar.gz
tar -xzf hadoop-2.6.0.tar.gz
sudo cp -a hadoop-2.6.0/. /usr/local/hadoop
sudo rm -r hadoop-2.6.0.tar.gz
sudo rm -r hadoop-2.6.0

echo "Copy the configuration files"
cp core-site.xml /usr/local/hadoop/etc/hadoop/
cp hadoop-env.sh /usr/local/hadoop/etc/hadoop/
cp mapred-site.xml /usr/local/hadoop/etc/hadoop/
cp hdfs-site.xml /usr/local/hadoop/etc/hadoop/
cp yarn-site.xml /usr/local/hadoop/etc/hadoop/

echo "Create necessary log files / folders and modify their access"
ssh hadoop101 "cp ~/.bashrc hadoop100"
sudo mkdir /usr/local/hadoop/logs
sudo chown toon:toon /usr/local/hadoop/logs
sudo chmod 777 -R /usr/local/hadoop/logs
sudo mkdir -p /home/toon/hadoopdata/hdfs/namenode
sudo mkdir -p /home/toon/hadoopdata/hdfs/datanode
sudo chmod 777 -R /home/toon/hadoopdata
sudo chown toon:toon /home/toon/hadoopdata

echo "Copy master and slaves file"
cp master /usr/local/hadoop/etc/hadoop
cp slaves /usr/local/hadoop/etc/hadoop

hdfs dfsadmin -safemode leave

hadoop namenode -format
start-dfs.sh
start-yarn.sh

hdfs dfs -mkdir /wc
hdfs dfs -copyFromLocal files /wc
hadoop jar wordcnt.jar WordCount /wc/files /out
