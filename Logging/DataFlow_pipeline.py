from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 26),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dataflow',
    default_args=default_args,
    description='A DAG for triggering a Dataflow job',
    schedule_interval=None, 
)


trigger_dataflow_task = DataflowTemplatedJobStartOperator(
    task_id='trigger_dataflow',
    template='gs://airflow-dags-leetsummarizer/templates/filter_logs',
    parameters={
        'input': 'gs://airflow-dags-leetsummarizer/input',
        'output': 'gs://airflow-dags-leetsummarizer/output'
    },
    location='us-central1',
    dag=dag,
)

trigger_dataflow_task