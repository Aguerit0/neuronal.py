from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow import DAG


default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id = 'dag_bash_operator_v03',
    default_args = default_args,
    description = 'DAG with BashOperator',
    start_date = datetime(2024, 9, 10),
    schedule_interval = timedelta(days=1),
    )as dag:
    task1 = BashOperator(
        task_id = 'task1',
        bash_command = 'ls',
    )
    task2 = BashOperator(
        task_id = 'task2',
        bash_command = 'mkdir example',
        )
    task3 = BashOperator(
        task_id = 'task3',
        bash_command = 'rm -r example',
    )
    task1 >> task2 >> task3