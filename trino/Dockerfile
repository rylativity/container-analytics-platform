FROM trinodb/trino:405

USER root

COPY ./etc/ /etc/trino/
RUN mkdir /var/trino && chown -R trino /etc/trino/ /var/trino

USER trino

# FROM azul/zulu-openjdk:11

# SHELL ["/bin/bash","-c"]

# ARG TRINO_SERVER_VERSION=395
# ARG HADOOP_VERSION=3.2.0

# RUN set -euxo pipefail && \
#      apt-get update && \
#       apt-get install -y \
#         python3 python3-dev python3-pip \
#         curl less &&\
#     ln -s /usr/bin/python3 /usr/bin/python &&\
#     echo "trino soft nofile 131072 \ntrino hard nofile 131072\n" >> /etc/security/limits.conf &&\
#     pip3 install sqlalchemy-trino && \
#     curl https://repo1.maven.org/maven2/io/trino/trino-server/${TRINO_SERVER_VERSION}/trino-server-${TRINO_SERVER_VERSION}.tar.gz -o /opt/trino-server.tar.gz && \
#     tar -xf /opt/trino-server.tar.gz -C /opt && rm -f /opt/trino-server.tar.gz && mv /opt/trino-server* /opt/trino && \
#     curl https://repo1.maven.org/maven2/io/trino/trino-cli/${TRINO_SERVER_VERSION}/trino-cli-${TRINO_SERVER_VERSION}-executable.jar -o /usr/bin/trino && \
#     useradd -m trino && \
#     chmod a+x /opt/trino/bin/launcher /usr/bin/trino && \
#     mkdir -p /var/trino/data/ && chown -R trino /var/trino /usr/bin/trino && chmod -R o+rwx /var/trino && \
#     mkdir /etc/hive_metastore && chown -R trino /etc/hive_metastore && \
#     curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/${HADOOP_VERSION}/hadoop-common-${HADOOP_VERSION}.jar -o /opt/trino/plugin/hive/hadoop-common-${HADOOP_VERSION}.jar && \
#     curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar -o /opt/trino/plugin/hive/hadoop-aws-${HADOOP_VERSION}.jar && \
#     curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.230/aws-java-sdk-bundle-1.12.230.jar -o /opt/trino/plugin/hive/aws-java-sdk-bundle-1.12.230.jar
# COPY conf /opt/trino/etc

# USER trino

# WORKDIR /opt/trino/

# CMD [ "bin/launcher", "run" ]

