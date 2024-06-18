from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.data_preprocessing.load_data import load_data
from src.data_preprocessing.handle_comments import remove_comments
from src.data_preprocessing.validate_code import validate_code
from src.data_preprocessing.validate_schema import validate_schema
from src.data_preprocessing.print_final_data import print_final_data
from src.data_preprocessing.dvc_pipeline import fetch_and_track_data

default_args = {
    'owner': 'sanket',
    'start_date': datetime(2024, 5, 18),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

def handle_failure(context):
    task_instance = context['task_instance']
    exception = task_instance.exception
    # Log or handle the exception as needed
    print(f"Task {task_instance.task_id} failed with exception: {exception}")

dag = DAG(
    'data_pipeline_v2',
    default_args=default_args,
    description='LeetSummarizer Data Pipeline',
    schedule_interval=None,
    catchup=False,
)

task_load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

task_validate_schema = PythonOperator(
    task_id='validate_schema',
    python_callable=validate_schema,
    op_args=[task_load_data.output],
    provide_context=True,
    dag=dag,
)

task_handle_comments = PythonOperator(
    task_id='handle_comments',
    python_callable=remove_comments,
    op_args=[task_validate_schema.output],
    provide_context=True,
    dag=dag,
)

task_validate_code = PythonOperator(
    task_id='validate_code',
    python_callable=validate_code,
    op_args=[task_handle_comments.output],
    provide_context=True,
    dag=dag,
)

task_print_final_data = PythonOperator(
    task_id='print_data',
    python_callable=print,
    op_args=[task_validate_code.output],
    provide_context=True,
    dag=dag,
)

task_dvc_pipeline = PythonOperator(
    task_id='update_dvc',
    python_callable=fetch_and_track_data,
    provide_context=True,
    dag=dag,
)



#Set up email notifications for success and failure
task_load_data >> task_validate_schema
task_validate_schema >> [task_handle_comments, task_validate_code]
task_handle_comments >> task_print_final_data
task_validate_code >> task_print_final_data
task_print_final_data >> task_dvc_pipeline

dag.on_failure_callback = handle_failure