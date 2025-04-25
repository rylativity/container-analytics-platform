# from airflow.decorators import dag
# from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
# from datetime import datetime

# GE_ROOT_DIR = "/opt/airflow/dags/dq/great_expectations"

# @dag(
#     dag_id="great_expectaions_dq_dag",
#     schedule="@once",  # Override to match your needs
#     start_date=datetime(2022, 1, 1),
#     catchup=False,
#     tags=["example"],
# )
# def great_expectations_dq():

#     ## This task will fail unless you create the source delta.my_schema.appl_stock_delta_table. 
#     # You can create this table by going to http://localhost:8888 and running the `pyspark_delta_example.ipynb` notebook
#     ge_data_context_root_dir_with_checkpoint_name_pass = GreatExpectationsOperator(
#     task_id="ge_data_context_root_dir_with_checkpoint_name_pass",
#     data_context_root_dir=GE_ROOT_DIR,
#     checkpoint_name="test_checkpoint",
#     return_json_dict = True,
# )

# great_expectations_dq()
    