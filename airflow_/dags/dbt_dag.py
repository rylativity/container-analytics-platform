from datetime import datetime
import os.path

from airflow.operators.bash import BashOperator
from airflow.decorators import dag

DBT_PROJECT_DIR = "/opt/airflow/dags/dbt_/project/my_project"
DBT_PROFILES_YAML_FILE = "/opt/airflow/dags/dbt_/project/profiles.yml"

@dag(
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
)
def dbt_dag():

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir {os.path.dirname(DBT_PROFILES_YAML_FILE)}"
    )

dbt_dag()