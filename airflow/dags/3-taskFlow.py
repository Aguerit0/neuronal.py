from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from sklearn.datasets import load_iris
import pandas as pd

@dag(
    dag_id = 'etl-taskflow-with-irisdata-v01',
    schedule_interval="@daily",
    start_date=datetime(2024, 10, 11),
    catchup=False,
    description="Un DAG ejemplo usando TaskFlow API con branching y control de flujo"
)
def etl_taskflow_with_real_data():

    @task
    def extract():
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        print("Extrayendo datos...")
        print(df.head())
        return df.to_dict(orient="records") 

    @task
    def transform(data):
        df = pd.DataFrame(data)
        df['normalized_sepal_length'] = df['sepal length (cm)'] / df['sepal length (cm)'].max()
        print(f"Transformando datos: Normalizando sepal length")
        return df.to_dict(orient="records")

    @task
    def check_data(data):
        df = pd.DataFrame(data)
        avg_value = df['normalized_sepal_length'].mean()
        print(f"Promedio del sepal length normalizado: {avg_value}")
        if avg_value > 0.5:
            print("Los datos son válidos para cargar.")
            return True
        else:
            print("Los datos no cumplen con los criterios para cargar.")
            return False

    @task.branch
    def decide_branch(is_valid):
        return 'load_data' if is_valid else 'skip_load'

    @task
    def load_data():
        print("datos cargados")

    skip_load = EmptyOperator(task_id="skip_load")

    data = extract()
    transformed_data = transform(data)
    is_valid = check_data(transformed_data)
    branch = decide_branch(is_valid)

    branch >> [load_data(), skip_load]

etl_dag = etl_taskflow_with_real_data()
