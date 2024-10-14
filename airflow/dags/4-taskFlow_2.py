"""
DESCRIPCIÓN
la idea es realizar una obtención del último precio (de alguna crypto),
aplicarle un indicador al precio para ver si existe una posible C/V
"""


from airflow.decorators import dag, task
from datetime import datetime, timedelta

import requests
import pandas as pd
#pip install pycoingecko matplotlib

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
        data_crypto = coinGecko.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)
        dates = [data[0] for data in data_crypto['prices']]
        dates = [
            datetime.datetime.fromtimestamp(date/1000)
            for date in dates
        ]
        prices = [data[1] for data in data_crypto['prices']]
        return pd.DataFrame({'date': dates, 'price': prices})
        
        
    @task
    def process_data(data):
        df = pd.DataFrame(data)