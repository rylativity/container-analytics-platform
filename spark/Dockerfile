FROM openjdk:11

ENV SPARK_VERSION=3.5.1
ENV SPARK_MAJOR_VERSION=3
ENV SPARK_HOME=/opt/spark

RUN apt-get update && apt-get install -y curl mlocate dumb-init

RUN curl -L https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${SPARK_MAJOR_VERSION}.tgz --output ./spark-${SPARK_VERSION}-bin-hadoop${SPARK_MAJOR_VERSION}.tgz && \
    tar zxvf ./spark-${SPARK_VERSION}-bin-hadoop${SPARK_MAJOR_VERSION}.tgz && mv spark-${SPARK_VERSION}-bin-hadoop${SPARK_MAJOR_VERSION} ${SPARK_HOME} && \
    rm -f ./spark-${SPARK_VERSION}-bin-hadoop${SPARK_MAJOR_VERSION}.tgz

ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

ENV SPARK_MASTER_IP=0.0.0.0