FROM bitnami/spark:3.3.0
ARG DELTA_LAKE_VERSION=2.1.0
ARG DELTA_CORE_VERSION=2.12
ARG FULL_VERSION=${DELTA_CORE_VERSION}-${DELTA_LAKE_VERSION}

ADD https://repo1.maven.org/maven2/io/delta/delta-core_${DELTA_CORE_VERSION}/${DELTA_LAKE_VERSION}/delta-core_${FULL_VERSION}.jar /opt/bitnami/spark/jars/delta-core_${FULL_VERSION}.jar