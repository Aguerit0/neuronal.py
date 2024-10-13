#connection_id
#database
#autocommit

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner':'airflow',
    'retries': 5,
    'retries_delay': timedelta(minutes=2)
}

with DAG(
    default_args = default_args,
    description = 'dag_postgres_operator',
    dag_id = 'dag_postgres_operator_v1',
    start_date = datetime(2024, 10, 10), 
    schedule_interval = '@daily',
)as dag:
    #create database
    task1 = PostgresOperator(
        task_id = 'task_create_database',
        postgres_conn_id = 'postgres_airflow',
        sql = 'CREATE DATABASE example_dag_db;',
        autocommit = True,
    )
    
    #create table
    task2 = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id = 'postgres_airflow',
        database = 'example_dag_db',
        sql = 'CREATE TABLE new_table_example (id serial primary key, name varchar(255),lastname varchar(255), age integer);',
        autocommit = True,
    )
    #select table
    task3 = PostgresOperator(
        task_id = 'select_table',
        postgres_conn_id = 'postgres_airflow',
        database = 'example_dag_db',
        sql = 'SELECT * FROM new_table_example;',
    )
    #insert table
    task4 = PostgresOperator(
        task_id = 'insert_table',
        postgres_conn_id = 'postgres_airflow',
        database = 'example_dag_db',
        autocommit = True,
        sql = 'INSERT INTO new_table_example(name, lastname, age) VALUES(%s, %s, %s);',
        parameters = ('Esteban', 'Aguero', 23),
    )
    
    task1>>task2>>task3>>task4

