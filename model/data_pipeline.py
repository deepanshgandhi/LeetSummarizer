from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from data_preprocessing import handle_comments, validate_code, validate_schema

# Define default_args
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'data_preprocessing_pipeline',
    default_args=default_args,
    description='A simple data preprocessing pipeline',
    schedule_interval=None
)

# Define Python callables for your functions
def run_handle_comments(**kwargs):
    handle_comments()

def run_validate_code(**kwargs):
    validate_code()

def run_validate_schema(**kwargs):
    validate_schema()

# Define the tasks
task_handle_comments = PythonOperator(
    task_id='handle_comments',
    python_callable=run_handle_comments,
    dag=dag,
)

task_validate_code = PythonOperator(
    task_id='validate_code',
    python_callable=run_validate_code,
    dag=dag,
)

task_validate_schema = PythonOperator(
    task_id='validate_schema',
    python_callable=run_validate_schema,
    dag=dag,
)

# Define the test tasks using BashOperator to run your test scripts
task_test_remove_comments = BashOperator(
    task_id='test_remove_comments',
    bash_command='pytest tests/test_remove_comments.py',
    dag=dag,
)

task_test_validate_code = BashOperator(
    task_id='test_validate_code',
    bash_command='pytest tests/test_validate_code.py',
    dag=dag,
)

# Define task dependencies
task_handle_comments >> task_validate_code >> task_validate_schema
task_handle_comments >> task_test_remove_comments
task_validate_code >> task_test_validate_code
