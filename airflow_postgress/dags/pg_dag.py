from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 4,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'create_database_v07',
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 10, 2),
) as dag:

    ''' task1 = PostgresOperator(
        task_id='task_create_database',
        postgres_conn_id='postgres_airflow',
        sql="CREATE DATABASE new_database_example;",
        autocommit=True,
    ) '''

    task2 = PostgresOperator(
        task_id='task_create_table',
        postgres_conn_id='postgres_airflow',
        database='new_database_example',

        sql="""
            CREATE TABLE IF NOT EXISTS new_table_example (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            );
        """,
        autocommit=True,
        
    )

    task3 = PostgresOperator(
    task_id='task_insert_data',
    postgres_conn_id='postgres_airflow',
    database='new_database_example',
    sql="INSERT INTO new_table_example (name) VALUES ('test');",
    autocommit=True,
)

    task4 = PostgresOperator(
        task_id='task_show_data',
        postgres_conn_id='postgres_airflow',
        database='new_database_example',
        sql="SELECT * FROM new_table_example;",
    )

    #task1 >> task2 >> task3 >> task4
    task2 >> task3 >> task4