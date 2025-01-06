from datetime import datetime
import logging
import os

from airflow import Dataset as AirflowDataset
from airflow.decorators import dag
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datahub_airflow_plugin.entities import Dataset as DatahubDataset, Urn

log = logging.getLogger(__name__)

SOURCE_CSV_DATA_PATH = f"s3a://test/transaction_data.csv"

BUCKET = "warehouse"
TABLE_NAME = "transaction_data"
BRONZE_TABLE_PATH = f"s3a://{BUCKET}/spark/bronze/{TABLE_NAME}"
SILVER_TABLE_PATH = f"s3a://{BUCKET}/spark/silver/{TABLE_NAME}"
GOLD_TABLE_PATH = f"s3a://{BUCKET}/spark/gold/{TABLE_NAME}"

spark_packages = 'org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-spark_2.12:3.1.0'


@dag(
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["bronze"],
)
def load_bronze_table():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    
    log.warn(f"Using Packages - {spark_packages}")
    
    spark_load_job = SparkSubmitOperator(
        application="/opt/airflow/dags/pyspark_apps/load_bronze_table_app.py", task_id="load_bronze_table",
        packages=spark_packages,
        # env_vars={},
        application_args=[f"--input-path={SOURCE_CSV_DATA_PATH}", f"--output-path={BRONZE_TABLE_PATH}"],
        inlets=[
            AirflowDataset(SOURCE_CSV_DATA_PATH), 
            DatahubDataset('s3', SOURCE_CSV_DATA_PATH)
            ],
        outlets=[
            AirflowDataset(BRONZE_TABLE_PATH), 
            DatahubDataset('s3',BRONZE_TABLE_PATH)
            ]
        # inlets={
        #     "tables":[SOURCE_CSV_DATA_PATH]
        # },
        # outlets={
        #     "tables":[BRONZE_TABLE_PATH]
        # }
    )
load_bronze_table()

@dag(
    schedule=[AirflowDataset(BRONZE_TABLE_PATH)],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["silver"],
)
def clean_and_load_silver_table():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    
    log.warn(f"Using Packages - {spark_packages}")
    
    spark_load_job = SparkSubmitOperator(
        application="/opt/airflow/dags/pyspark_apps/clean_and_load_silver_table_app.py", task_id="clean_and_load_silver_table",
        packages=spark_packages,
        env_vars={},
        application_args=[f"--input-path={BRONZE_TABLE_PATH}", f"--output-path={SILVER_TABLE_PATH}"],
        outlets=[AirflowDataset(SILVER_TABLE_PATH)]
    )
clean_and_load_silver_table()

@dag(
    schedule=[AirflowDataset(SILVER_TABLE_PATH)],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["silver"],
)
def process_and_load_gold_table():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    
    log.warn(f"Using Packages - {spark_packages}")
    
    spark_load_job = SparkSubmitOperator(
        application="/opt/airflow/dags/pyspark_apps/process_and_load_gold_table_app.py", task_id="process_and_load_gold_table",
        packages=spark_packages,
        # env_vars={},
        application_args=[f"--input-path={SILVER_TABLE_PATH}", f"--output-path={GOLD_TABLE_PATH}"],
        outlets=[AirflowDataset(GOLD_TABLE_PATH)]
    )
process_and_load_gold_table()
