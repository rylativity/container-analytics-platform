#!/bin/sh

export HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
export HADOOP_CLASSPATH=${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk-bundle-1.11.375.jar:${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws-${HADOOP_VERSION}.jar
export JAVA_HOME=/usr/local/openjdk-8

/opt/apache-hive-metastore-${METASTORE_VERSION}-bin/bin/schematool -initSchema -dbType postgres
/opt/apache-hive-metastore-${METASTORE_VERSION}-bin/bin/start-metastore