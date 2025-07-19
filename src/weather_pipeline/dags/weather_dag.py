from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "weather_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    BashOperator(task_id="hello", bash_command="echo 'Hello Airflow'")
