from airflow.decorators import task, dag
from airflow.providers.trino.operators.trino import TrinoOperator
from datetime import datetime


#### NOTE!!!!!
## You must create an Airflow connection for Trino before running this dag.
#  Open http://localhost:8080, login with username:airflow and password:airflow
# Go to Admin > Connections, and create a new connection with the information below:
# connection_id=trino_default, host=trino, schema=default, login=trino, port=8080

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

    trino_create_schema = TrinoOperator(
        task_id="trino_create_schema",
        sql=f"CREATE SCHEMA IF NOT EXISTS {SCHEMA} WITH (location='s3a://test/')",
        handler=list
    )


    ## This task will fail unless you create the source delta.my_schema.appl_stock_delta_table. 
    # You can create this table by going to http://localhost:8888 and running the `pyspark_delta_example.ipynb` notebook
    trino_create_table = TrinoOperator(
        task_id="trino_create_table",
        sql=f"""CREATE TABLE IF NOT EXISTS appl_stock_delta_table2 AS(
        SELECT * FROM {DB}.{SCHEMA}.appl_stock_delta_table
        )""",
        handler=list,
    )

    trino_create_schema >> trino_create_table

trino_dag()
    
