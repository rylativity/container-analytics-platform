FROM bitnami/spark:3.3.0
ARG DELTA_CORE_VERSION=2.12-2.1.0
RUN curl https://repo1.maven.org/maven2/io/delta/delta-core_2.13/2.1.0/delta-core_${DELTA_CORE_VERSION}.jar --output /opt/bitnami/spark/jars/delta-core_${DELTA_CORE_VERSION}.jar