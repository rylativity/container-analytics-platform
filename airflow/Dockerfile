FROM apache/airflow:3.0.0-python3.12

USER root 

RUN apt-get update && apt-get install -y openjdk-17-jdk && rm -rf /var/lib/apt/lists

USER airflow

COPY requirements.txt .

RUN pip install -r requirements.txt

# COPY airflow.cfg /opt/airflow/airflow.cfg

#_________________________________#
# ARG AIRFLOW_VERSION=3.0.0
# FROM apache/airflow:${AIRFLOW_VERSION}

# ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.12.txt"
# ARG AIRFLOW_USE_UV="true"
# ENV AIRFLOW_USE_UV=${AIRFLOW_USE_UV}

# RUN uv pip install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" \
#     apache-airflow-providers-trino[common.sql] \
#     pyspark==3.5.5 \
#     apache-airflow-providers-apache-spark \
#     deltalake \
#     acryl-datahub-airflow-plugin[plugin-v2] 


#_________________________________#

# ARG PYTHON_VERSION=3.12
# FROM python:${PYTHON_VERSION}-alpine

# ARG AIRFLOW_VERSION=3.0.0

# ENV UV_BUILD_CONSTRAINT=https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt
# ENV AIRFLOW_HOME=~/airflow

# # Download the latest installer
# ADD https://astral.sh/uv/install.sh /uv-installer.sh

# # Run the installer then remove it
# RUN sh /uv-installer.sh && rm /uv-installer.sh \
#     && apk add gcc musl-dev linux-headers bash

# # Ensure the installed binary is on the `PATH`
# ENV PATH="/root/.local/bin/:$PATH"

# WORKDIR ${AIRFLOW_HOME}
# RUN uv init && uv add "apache-airflow==${AIRFLOW_VERSION}"

# ENV PATH="${AIRFLOW_HOME}/.venv/bin:$PATH"

# COPY entrypoint.sh /entrypoint

# ENTRYPOINT [ "uv", "run", "airflow" ]
# CMD ["standalone"]
