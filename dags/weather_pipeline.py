from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine
import os
import json

def extract_weather_data(api_key, lat, lon, **kwargs):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    weather_data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_data_path = f"/opt/airflow/data/raw/weather_data_{timestamp}.json"
    with open(raw_data_path, "w") as f:
        json.dump(weather_data, f)

    kwargs["ti"].xcom_push(key="raw_weather_data", value=weather_data)

def transform_weather_data(**kwargs):
    ti = kwargs["ti"]
    raw_weather_data = ti.xcom_pull(key="raw_weather_data", task_ids="extract_weather_data")

    timestamp = raw_weather_data["dt"]
    date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    temp = raw_weather_data["main"]["temp"]
    humidity = raw_weather_data["main"]["humidity"]

    df = pd.DataFrame([{
        "datetime": date,
        "temperature_celsius": temp,
        "humidity_percent": humidity
    }])

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    transformed_data_path = f"/opt/airflow/data/processed/transformed_weather_data_{ts}.csv"
    df.to_csv(transformed_data_path, index=False)

    ti.xcom_push(key="transformed_weather_df", value=df.to_json())

def load_weather_data(**kwargs):
    ti = kwargs["ti"]
    df_json = ti.xcom_pull(key="transformed_weather_df", task_ids="transform_weather_data")
    df = pd.read_json(df_json)

    db_connection_str = "postgresql+psycopg2://user:password@data-db:5432/weather_data"
    engine = create_engine(db_connection_str)

    df.to_sql("current_weather", engine, if_exists="append", index=False)

with DAG(
    dag_id="weather_data_pipeline",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["weather", "etl", "docker"],
) as dag:
    extract_task = PythonOperator(
        task_id="extract_weather_data",
        python_callable=extract_weather_data,
        op_kwargs={
            "api_key": os.getenv("OPENWEATHER_API_KEY"),
            "lat": -23.55052,
            "lon": -46.633308,
        },
    )

    transform_task = PythonOperator(
        task_id="transform_weather_data",
        python_callable=transform_weather_data,
    )

    load_task = PythonOperator(
        task_id="load_weather_data",
        python_callable=load_weather_data,
    )

    extract_task >> transform_task >> load_task
