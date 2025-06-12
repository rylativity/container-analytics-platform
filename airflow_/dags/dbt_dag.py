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

    dbt_task = BashOperator(
        task_id="dbt_task",
        bash_command=f"dbt build --project-dir {DBT_PROJECT_DIR} --profiles-dir {os.path.dirname(DBT_PROFILES_YAML_FILE)}"
    )

dbt_dag()