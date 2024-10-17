"""
Descripción del Proyecto: Predicción de Señales de Compra/Venta de Criptomonedas
El proyecto consiste en la creación de un sistema automatizado para la extracción y análisis de datos del mercado de criptomonedas, aplicando indicadores técnicos para generar señales de compra/venta. Utilizando la API de Binance, el sistema obtiene los datos históricos de precios de Bitcoin (u otras criptomonedas), calcula el índice RSI (Relative Strength Index) y almacena los resultados en una base de datos para su posterior análisis. El flujo de trabajo se orquesta con Airflow, y la integración con AWS permite escalabilidad, monitoreo y almacenamiento temporal para asegurar la confiabilidad del sistema.

Motivación del Uso de S3: Los datos procesados se almacenan temporalmente en Amazon S3 como una medida para manejar de forma segura la llegada de información final a la base de datos. De esta manera, si ocurre un error en el proceso de almacenamiento en RDS, los datos siguen disponibles en S3 y pueden recuperarse sin necesidad de volver a procesar o extraer datos desde la API de Binance.

Pasos del Proyecto:
- Extracción de datos: Se utiliza una función Lambda para obtener datos de precios desde la API de Binance. Los datos se almacenan temporalmente en S3 para asegurar la persistencia de la información.
- Procesamiento de datos: Lambda procesa los datos almacenados en S3, aplicando el cálculo del indicador RSI.
- Almacenamiento final: Los resultados de RSI se almacenan en una base de datos administrada en Amazon RDS (PostgreSQL), donde se mantendrán para análisis y consulta.
- Monitoreo y Alertas: CloudWatch monitoriza la ejecución de las funciones Lambda y el estado de la base de datos RDS, generando alertas si ocurre algún fallo. Opcionalmente, se pueden enviar notificaciones por medio de Amazon SNS.
- Orquestación: Airflow se utiliza para orquestar la secuencia de tareas, permitiendo la ejecución automatizada diaria de las funciones de extracción, procesamiento y almacenamiento.
"""


from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
#import sensor airflow
from airflow.providers.common.sql.sensors.sql import SqlSensor
#? airflow.sensors.sql import SqlSensor

import requests
import pandas as pd

from binance import Client
binance_client = Client()
period = 14 #for rsi


@dag(
    dag_id = 'taskflow_v01',
    schedule_interval = '@daily',
    start_date = datetime(2024, 10, 11),
    description = 'example dag',
)


def etl_btc_data():
    #task-1: extract btc price data from binance api
    @task(task_id = 'extract_btc_price')
    def extract_btc_price():
        ohlcv_data = binance_client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1DAY, limit=30)
        
        # Extraer y estructurar los datos
        df = pd.DataFrame(ohlcv_data, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume", "ignore"
        ])
        
        # Convertir el timestamp a un formato legible
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')

        print(df.head())
        return df
        
    #task-2: calculate rsi value
    @task(task_id = 'calculate_rsi')
    def calculate_rsi(data):
        df = data.copy()
        df["close"] = df["close"].astype(float)
        delta = df["close"].diff()

        up, down = delta.clip(lower=0), delta.clip(upper=0).abs()
        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.ewm(com=(period - 1), min_periods=period).mean()

        RS = _gain / _loss
        rsi = 100 - (100 / (1 + RS))

        return rsi.iloc[-1]  # return rsi series

    #task-3: check signal buy/sell rsi
    @task(task_id = 'check_signal')
    def checksignal(rsi):
        if rsi < 30:
            return 0 #0 = buy
        elif rsi > 70:
            return 1 #1 = sell
        else:
            return 2 #2 = hold
    
    
    #add sensor for the task 4
    sensor_check_exist_db = SqlSensor(
        task_id = 'check_exist_db',
        conn_id = 'postgres_airflow',
        sql = 'SELECT EXISTS (SELECT 1 FROM pg_database WHERE datname = \'signal_rsi_db\')',
        mode = 'poke',
        poke_interval = 10,
        timeout = 600,
    )
    
    #task-4: save signal in database
    @task(task_id = 'db_create')
    def db_create(signal):
        postgres_conn_id = 'postgres_airflow'
        sql = "CREATE DATABASE signal_rsi_db;"
        autocommit = True
    

    #add sensor for the task 5
    sensor_check_exist_table = SqlSensor(
        task_id = 'check_exist_table',
        conn_id = 'postgres_airflow',
        sql = 'SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = \'rsi_data\')',
        mode = 'poke',
        poke_interval = 10,
        timeout = 600,
    )   
    #task-5: create table in database
    @task(task_id = 'create_table')
    def create_table():
        postgres_conn_id = 'postgres_airflow'
        database = 'signal_rsi_db'
        sql = "CREATE TABLE rsi_data (rsi float);"
        autocommit = True
    
    #task-6: insert data in table
    @task(task_id = 'insert_data')
    def insert_data(rsi):
        postgres_conn_id = 'postgres_airflow'
        database = 'signal_rsi_db'
        sql = "INSERT INTO rsi_data (rsi) VALUES (%s);"
        autocommit = True
    
    #task-7: select data in table
    @task(task_id = 'select_data')
    def select_data():
        postgres_conn_id = 'postgres_airflow'
        database = 'signal_rsi_db'
        sql = "SELECT * FROM rsi_data;"
    
    
    #running tasks
    data = extract_btc_price()
    rsi = calculate_rsi(data)

    sensor_check_exist_db >> db_create()

    sensor_check_exist_table >> create_table()

    insert_data(signal)
    select_data()
        

etl_btc_data()