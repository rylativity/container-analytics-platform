FROM apache/airflow:2.5.3-python3.9

USER root 

RUN apt-get update && apt-get install -y openjdk-11-jdk && rm -rf /var/lib/apt/lists

USER airflow

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY airflow.cfg /opt/airflow/airflow.cfg
