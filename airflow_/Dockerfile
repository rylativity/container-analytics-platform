FROM apache/airflow:2.5.3-python3.10

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY airflow.cfg /opt/airflow/airflow.cfg
