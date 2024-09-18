from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 16),
    'retries': 1
}

dag = DAG(
    'mongo_query_dag',
    default_args=default_args,
    description='DAG que consulta MongoDB',
    schedule_interval='@daily', 
)

mongo_query_task = BashOperator(
    task_id='mongo_query',
    bash_command='python /path/to/your/query_mongodb.py',
    dag=dag
)

mongo_query_task