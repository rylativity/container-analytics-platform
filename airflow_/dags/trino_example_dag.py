from airflow.decorators import task, dag
from airflow.providers.trino.operators.trino import TrinoOperator
from datetime import datetime


#### NOTE!!!!!
## THIS DAG REQUIRES DATA THAT IS CREATED BY THE `pyspark_delta_example.ipynb` notebook in the jupyter/notebooks folder

SCHEMA = "my_schema"
DB = "delta"

@dag(
    dag_id="example_trino",
    schedule="@once",  # Override to match your needs
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["example"],
)
def trino_dag():

    trino_create_table = TrinoOperator(
        trino_conn_id="Trino",
        task_id="trino_create_table",
        sql=f"""CREATE TABLE IF NOT EXISTS appl_stock_delta_table2 AS(
        SELECT * FROM {DB}.{SCHEMA}.appl_stock_delta_table
        )""",
        handler=list,
    )

trino_dag()
    
