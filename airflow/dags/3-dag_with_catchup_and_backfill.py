#	•	Catchup se refiere a cuando Airflow automáticamente se pone al día con las ejecuciones omitidas desde la fecha de inicio hasta la fecha actual.
#	•	Backfill es el proceso manual o automático de ejecutar tareas para fechas anteriores
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 9, 18),
}

with DAG(
    dag_id='dag_with_catchup_and_backfill_v02',
    default_args = default_args,
    description = 'DAG with catchup and backfill',
    schedule_interval = '@daily',
    catchup = False
    
    ) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "task1"',
    )
    task2 = BashOperator(
        task_id='task2',
        bash_command='echo "task2"'
    )
    task3 = BashOperator(
        task_id='task3',
        bash_command='echo "task3"'
    )
    task1 >> [task2, task3]