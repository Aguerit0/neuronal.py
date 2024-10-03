from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow import DAG

default_args = {
    'owner': 'airflow',
    'description': 'DAG con PostgresOperator',
    'retries': 5,
    'retries_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id= 'dag_postgres_v01',
    start_Date = datetime(2024, 10, 3),
    schedule_interval='@daily',
)as dag:
    #task1 : create database
    task1 = PostgresOperator(
        task_id = 'task_create_database',
        postgres_conn_id = 'postgres_airflow',
        autocommit = True,
        sql = 'create database IF NOT EXISTS database_dag_example;',
    )
    #task2 : create table
    task2 = PostgresOperator(
        task_id = 'task_create_table',
        postgres_conn_id='postgres_airflow',
        autocommit = True,
        database = 'database_dag_example',
        sql = 'create table new_table_example(id serial primary key, name varchar(255), age integer);',
    )
    # task3 : select data
    task3 = PostgresOperator(
        task_id = 'task_select_data',
        postgres_conn_id='postgres_airflow',
        database = 'database_dag_example',
        sql = 'SELECT * FROM new_table_example;',
    )
    # task4 : insert data
    task4 = PostgresOperator(
        task_id = 'task_insert_data',
        postgres_conn_id='postgres_airflow',
        database = 'database_dag_example',
        sql = 'INSERT INTO new_table_example(name, age) VALUES(%s, %s);',
        parameters = ('John', 32),
    )
    task1 >> task2 >> task3 >> task4 >> task3
