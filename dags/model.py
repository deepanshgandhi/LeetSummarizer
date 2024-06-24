from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.vertex_ai import VertexAIModelTrainingOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 6, 19),
}

dag = DAG('model_training_workflow_vertex_ai',
          default_args=default_args,
          description='Trigger model training on Vertex AI',
          schedule_interval=None)

train_model_task = VertexAIModelTrainingOperator(
    task_id='train_model_task',
    project_id='your-project-id',
    location='us-central1',  # Choose appropriate location
    display_name='your-model-training-job',
    container_uri='gcr.io/your-project-id/your-training-container:latest',  # Docker image with training code
    model_serving_container_image_uri='gcr.io/your-project-id/your-serving-container:latest',  # Docker image for serving
    staging_bucket='gs://your-staging-bucket',  # Cloud Storage bucket for job artifacts
    python_package_gcs_uri='gs://your-bucket/path/to/your/package.tar.gz',  # Path to Python package containing training script
    machine_type='n1-standard-8',  # Specify machine type with GPU (e.g., n1-standard-8 with T4)
    accelerator_type='NVIDIA_TESLA_T4',  # Specify GPU type
    accelerator_count=1,  # Number of GPUs
    cmd=['python', 'train_model.py', '--data_path', 'gs://your-data-bucket/preprocessed_data.json'],
    dag=dag,
)