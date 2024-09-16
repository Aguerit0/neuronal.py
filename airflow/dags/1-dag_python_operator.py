from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# configurations for DAG
default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# functions for tasks
def get_name():
    return 'Esteban'

def get_age():
    return 23

def hello_dag():
    print(f'Hello {get_name()} you are {get_age()} years old')

with DAG(
    dag_id='python_operator_dag_v02',
    description='DAG with PythonOperator',
    default_args=default_args,
    start_date=datetime(2024, 9, 10),
    schedule_interval=timedelta(days=1),
) as dag:
    
    task1 = PythonOperator(
        task_id='task1',
        python_callable=get_name,
    )
    
    task2 = PythonOperator(
        task_id='task2',
        python_callable=get_age,
    )
    
    task3 = PythonOperator(
        task_id='task3',
        python_callable=hello_dag,
    )

    # Define la secuencia de tareas
    [task1, task2] >> task3