from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner' : 'airflow',
    'retries' : 5,
    'retries_delay' : timedelta(minutes=1)
}

def get_name():
    return 'Esteban'

def get_age ():
    return 23

with DAG(
    dag_id = 'operators_v01',
    description = 'primer dag',
    start_date = datetime(2024, 9, 20),
    schedule_interval = '@daily',
    default_args = default_args
)as dag:
    task1 = PythonOperator(
        task_id = 'get_name',
        python_callable = get_name
    )
    task2 = PythonOperator(
        task_id = 'get_age',
        python_callable = get_age
    )
    
    task2 >> task1


