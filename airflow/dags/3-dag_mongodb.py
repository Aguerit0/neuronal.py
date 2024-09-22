from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
import requests
from pymongo import MongoClient

import json
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 17),
    'retries': 1
}

def extract():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(url)
    return response.json()

def transform(ti):
    data = ti.xcom_pull(task_ids='extract')
    return {"coin": "bitcoin", "price": data['bitcoin']['usd'], "date": datetime.now()}
    
def load(ti):
    data = ti.xcom_pull(task_ids='transform')
    # Mongo db container
    client = MongoClient('http://localhost:27017/')
    db = client['coinmgecko_db']
    collection = db['prices']
    collection.insert_one(data)


with DAG(
    'mongo_etl_dag_v01',
    default_args=default_args,
    description='DAG que consulta MongoDB',
    schedule_interval='@daily', 
) as dag:
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform
    )
    load_task = PythonOperator(
        task_id='load',
        python_callable=load
    )
    extract_task >> transform_task >> load_task
    