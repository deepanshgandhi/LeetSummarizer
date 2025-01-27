from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.google.cloud.hooks.compute_ssh import ComputeEngineSSHHook
from airflow.providers.ssh.hooks.ssh import SSHHook

from src.data_preprocessing.load_data import load_data
from src.data_preprocessing.handle_comments import remove_comments
from src.data_preprocessing.validate_code import validate_code
from src.data_preprocessing.validate_schema import validate_schema
from src.data_preprocessing.print_final_data import print_final_data
from src.data_preprocessing.dvc_pipeline import fetch_and_track_data
from src.data_preprocessing.success_email import send_success_email
from src.data_preprocessing.failure_email import send_failure_email

default_args = {
    'owner': 'rahul',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

GCE_INSTANCE = 'leetsummarizer'
GCE_ZONE = 'us-west4-a'
GCP_PROJECT_ID = 'leetsummarizer'

ssh_hook = SSHHook(ssh_conn_id='ssh_vm')

# Function to handle failur
def handle_failure(context):
    task_instance = context['task_instance']
    exception = task_instance.exception
    # Log or handle the exception as needed
    print(f"Task {task_instance.task_id} failed with exception: {exception}")
    try:
        send_failure_email(task_instance, exception)
        print("Failure email sent successfully!")
    except Exception as e:
        print(f"Error sending failure email: {e}")

# Define the DAG
dag = DAG(
    'pipeline',
    default_args=default_args,
    description='LeetSummarizer Data Pipeline',
    schedule_interval=timedelta(days=1),  # Run once a day
    catchup=False,
)

task_load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
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
    python_callable=print_final_data,
    op_args=[task_validate_code.output],
    op_kwargs={
            'bucket_name': 'airflow-dags-leetsummarizer',
            'destination_blob_name': 'dags/data/preprocessed_data.json'
        },
    provide_context=True,
    dag=dag,
)

task_dvc_pipeline = PythonOperator(
    task_id='update_dvc',
    python_callable=fetch_and_track_data,
    provide_context=True,
    dag=dag,
)


task_send_email = PythonOperator(
    task_id='task_send_email',
    python_callable=send_success_email,
    provide_context = True,
    dag=dag,
)



ssh_task_train = SSHOperator(
    task_id="ssh_task_train",
    ssh_hook=ComputeEngineSSHHook(
        user="199512703680-compute@developer.gserviceaccount.com",
        instance_name=GCE_INSTANCE,
        zone=GCE_ZONE,
        project_id=GCP_PROJECT_ID,
        use_oslogin=True,
        use_iap_tunnel=False
    ),
    command="cd /; sudo docker-compose -f docker-compose-train.yml -p leetsummarizer down; sudo docker-compose -f docker-compose-train.yml -p leetsummarizer pull; sudo docker-compose -f docker-compose-train.yml -p leetsummarizer up -d",
    cmd_timeout = 6000,
    dag=dag
)

ssh_task_app = SSHOperator(
    task_id="ssh_task_app",
    ssh_hook=ComputeEngineSSHHook(
        user="199512703680-compute@developer.gserviceaccount.com",
        instance_name=GCE_INSTANCE,
        zone=GCE_ZONE,
        project_id=GCP_PROJECT_ID,
        use_oslogin=True,
        use_iap_tunnel=False
    ),
    command="cd /; sudo docker-compose -f docker-compose-app.yml -p leetsummarizer down; sudo docker-compose -f docker-compose-app.yml -p leetsummarizer pull; sudo docker-compose -f docker-compose-app.yml -p leetsummarizer up -d",
    cmd_timeout = 6000,
    dag=dag
)

# Set up task dependencies
task_load_data >> task_validate_schema
task_validate_schema >> [task_handle_comments, task_validate_code]
task_handle_comments >> task_print_final_data
task_validate_code >> task_print_final_data
task_print_final_data >> task_dvc_pipeline
task_dvc_pipeline >> ssh_task_train >> ssh_task_app >> task_send_email


# Set up the failure callback
dag.on_failure_callback = handle_failure





# task_validate_code = PythonOperator(
#     task_id='validate_code',
#     python_callable=validate_code,
#     dag=dag,
# )

# task_validate_schema = PythonOperator(
#     task_id='validate_schema',
#     python_callable=validate_schema,
#     dag=dag,
# )




