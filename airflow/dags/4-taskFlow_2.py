from airflow.decorators import dag, task
from datetime import datetime, timedelta

import requests
import pandas as pd
import pycoingecko


#initialize coingecjo api client
coinGecko = pycoingecko.CoinGeckoAPI()
#get historical price brc
data = 

@dag(
    dag_id = 'taskflow_v01',
    schedule_interval = '@daily',
    start_date = datetime(2024, 10, 11),
    description = 'example dag',
)


def etl_btc_data():
    @task
    def extract_btc_price():
        return requests.get(API).json()['bitcoin']
    
    
    @task
    def process_data(data):
        