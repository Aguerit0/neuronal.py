"""
-create bucket s3: https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html#creating-bucket
-create iam role to acces bucket: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.Authorizing.IAM.S3CreatePolicy.html
-get credentials: https://docs.aws.amazon.com/es_es/cli/latest/userguide/cli-configure-files.html

IMPORTANT
1- config aws cli = aws configure -> terminal
2- create credentials file

"""

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import pandas as pd
import requests
import boto3
from io import StringIO
from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME, REGION_NAME, OBJECT_NAME


@dag(
    dag_id = 'dag_taskflow',
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2024, 11, 17),
    catchup=False,
    description="Example DAG using TaskFlow",
    max_active_runs=1
)


#task-1: extract data from api binance
def etl_btc_data():
    @task(task_id='extract_btc_price')
    def extract_btc_price():
        URL_API_BINANCE = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100'
        response = requests.get(URL_API_BINANCE)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        # Serialize DataFrame to JSON for task transfer
        return df.to_json(orient="records")
    
    # Task 2: Upload data to S3
    @task(task_id='upload_to_s3')
    def upload_to_s3(data_json):
        if data_json:
            s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
            bucket_name = BUCKET_NAME
            object_name = OBJECT_NAME

            # Convert JSON back to DataFrame
            signals_df = pd.read_json(data_json, orient="records")
            
            try:
                # Check if file exists in S3 and load existing data
                response = s3.get_object(Bucket=bucket_name, Key=object_name)
                existing_df = pd.read_csv(response['Body'])
                updated_df = pd.concat([existing_df, signals_df], ignore_index=True)
            except s3.exceptions.NoSuchKey:
                updated_df = signals_df  # No existing file, use the current DataFrame
            except Exception as e:
                print(f"Error reading S3 file: {e}")
                return  # Stop if there's an error

            # Write updated DataFrame back to S3 as CSV
            csv_buffer = StringIO()
            updated_df.to_csv(csv_buffer, index=False)
            s3.put_object(Bucket=bucket_name, Key=object_name, Body=csv_buffer.getvalue())
            print("Signals exported to S3 successfully.")

    # Task 3: Extract data from S3
    @task(task_id='extract_from_s3')
    def extract_from_s3():
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
        bucket_name = BUCKET_NAME
        object_name = OBJECT_NAME

        try:
            response = s3.get_object(Bucket=bucket_name, Key=object_name)
            return response['Body'].read().decode('utf-8')
        except s3.exceptions.NoSuchKey:
            return None

    # DAG Execution
    data_json = extract_btc_price()
    upload_to_s3(data_json)
    extract_from_s3()


etl_btc_data = etl_btc_data()