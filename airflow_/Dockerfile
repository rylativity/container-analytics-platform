FROM apache/airflow:2.9.2-python3.10

USER root 

RUN apt-get update && apt-get install -y openjdk-17-jdk && rm -rf /var/lib/apt/lists

USER airflow

COPY requirements.txt .

RUN pip install -r requirements.txt

# COPY airflow.cfg /opt/airflow/airflow.cfg
