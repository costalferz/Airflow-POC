from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_data():
    # Fetch data from the URL
    url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-line-lists"

    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("./data/data.csv", index=False)

def upload_data_to_discord():
    # Define the Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/"+ os.environ.get("webhook_url")
    
    # Read the CSV file
    df = pd.read_csv("./data/data.csv")

    # Convert DataFrame to CSV and get CSV data
    csv_data = df.to_csv(index=False).encode()

    # Create the payload to send to the webhook
    payload = {
        'file': ('data.csv', csv_data)
    }

    # Send the payload to the webhook
    response = requests.post(webhook_url, files=payload)

    # Check the response status
    if response.status_code == 200:
        print("CSV file uploaded to Discord webhook successfully.")
    else:
        print("Failed to upload CSV file to Discord webhook.")

default_args = {
    'owner': 'kanatip',
    'start_date': datetime(2024, 1, 14),
}

dag = DAG('discord_test',
         schedule_interval='@daily',
         default_args=default_args,
         description='A simple data pipeline for COVID-19 report',
         start_date=datetime(2022, 1, 1),
         catchup=False)

t1 = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag
)

t2 = PythonOperator(
    task_id='upload_data_to_discord',
    python_callable=upload_data_to_discord,
    dag=dag
)

# Set task dependencies
t1 >> t2