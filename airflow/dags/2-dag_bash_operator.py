# mkdir -pv /tmp/example
# echo "Hola, mundo!" > /tmp/example/output.txt
# ls /tmp/example
# rm -r /tmp/example
# trigger_rule = 'all_success',

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retries_delay': timedelta(minutes=1)
}

with DAG(
    dag_id = 'dag_bash_2',
    description = 'dag_bash',
    start_date = datetime(2024, 9, 25),
    schedule_interval = '@daily',
    default_args = default_args,
)as dag:
    task1 = BashOperator(
        task_id = 'task_mkdir',
        bash_command = 'mkdir -pv /tmp/example',
    )
    task2 = BashOperator(
        task_id = 'task_echo',
        bash_command = 'echo "Hola, mundo!" > /tmp/example/output.txt',
    )
    task3 = BashOperator(
        task_id = 'task_ls',
        bash_command = 'ls /tmp/example',
    )
    task4 = BashOperator(
        task_id = 'task_remove',
        bash_command = 'rm -r /tmp/example',
    )
    
    task1 >> task2 >> task3 >> task4