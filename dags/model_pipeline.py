from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import aiplatform
from google.cloud import notebooks_v1
from datetime import datetime, timedelta
import time
import json
from google.cloud import storage

def load_data_from_gcs(bucket_name, file_path):
    """Load JSON data from Google Cloud Storage
    
    Args:
        bucket_name (str): The name of the bucket
        file_path (str): The path to the file in the bucket
    """
    # Initialize a client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Get the blob (file) from the bucket
    blob = bucket.blob(file_path)

    # Download blob as a string
    data = blob.download_as_string()

    # Parse the JSON data
    json_data = json.loads(data)

    return json_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'vertex_ai_notebook',
    default_args=default_args,
    description='Run model training on Vertex AI using Airflow',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

def execute_notebook():
    # Initialize the Vertex AI and Notebooks API clients
    aiplatform.init(project='leetsummarizer', location='us-west4')
    notebook_service = notebooks_v1.NotebookServiceClient()

    # Specify the instance details
    project_id = 'leetsummarizer'
    location = 'us-west4'

    # Define the notebook file to be executed
    notebook_file = load_data_from_gcs('airflow-dags-leetsummarizer', 'model/model_train.ipynb')

    # Construct the name of the notebook instance
    name = "model-training-notebook"

    # Create an execution request
    execution_request = {
        "name": name,
        "input_notebook_file": notebook_file,
        "parameters": {},
    }

    # Submit the execution request
    execution = notebook_service.execute_notebook(execution_request)

    # Wait for execution to complete
    execution_name = execution.name
    while True:
        execution = notebook_service.get_execution(name=execution_name)
        if execution.state == notebooks_v1.Execution.State.SUCCEEDED:
            print("Notebook execution succeeded")
            break
        elif execution.state == notebooks_v1.Execution.State.FAILED:
            print("Notebook execution failed")
            break
        else:
            print("Notebook execution in progress...")
            time.sleep(30)

run_notebook_task = PythonOperator(
    task_id='run_notebook_task',
    python_callable=execute_notebook,
    dag=dag,
)

run_notebook_task