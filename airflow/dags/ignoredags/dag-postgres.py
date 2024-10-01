from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='mi_dag_postgres_v02',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
) as dag:
    t1 = SQLExecuteQueryOperator(
    task_id='select_datos',
    sql='SELECT * FROM cancer_data',  # Cambia el nombre de la tabla por la tuya
    conn_id='postgresSQL',  # Nombre de la conexión que creaste
    dag=dag
)