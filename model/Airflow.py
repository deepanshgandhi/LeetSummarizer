from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Importing functions from your main.py script
from update_model_func import install_dependencies, load_packages, load_model, configure_model, \
                                prepare_dataset, train_model, generate_response

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'model_pipeline',
    default_args=default_args,
    description='DAG for running model pipeline',
    schedule_interval=timedelta(days=1),
) as dag:

    # Task 1: Install Dependencies
    install_deps_task = PythonOperator(
        task_id='install_dependencies',
        python_callable=install_dependencies,
    )

    # Task 2: Load Packages
    load_packages_task = PythonOperator(
        task_id='load_packages',
        python_callable=load_packages,
    )

    # Task 3: Load Model
    load_model_task = PythonOperator(
        task_id='load_model',
        python_callable=load_model,
        op_kwargs={'model_name': 'unsloth/mistral-7b-v0.3-bnb-4bit'},
    )

    # Task 4: Configure Model
    configure_model_task = PythonOperator(
        task_id='configure_model',
        python_callable=configure_model,
        op_kwargs={
            'model': '{{ ti.xcom_pull(task_ids="load_model", key="return_value")[0] }}',
        },
    )

    # Task 5: Prepare Dataset
    prepare_dataset_task = PythonOperator(
        task_id='prepare_dataset',
        python_callable=prepare_dataset,
        op_kwargs={
            'prompt': "Summarize the provided code solution...",
            'tokenizer': '{{ ti.xcom_pull(task_ids="load_model", key="return_value")[1] }}',
        },
    )

    # Task 6: Train Model
    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        op_kwargs={
            'model': '{{ ti.xcom_pull(task_ids="load_model", key="return_value")[0] }}',
            'tokenizer': '{{ ti.xcom_pull(task_ids="load_model", key="return_value")[1] }}',
            'dataset': '{{ task_instance.xcom_pull(task_ids="prepare_dataset") }}',
        },
    )

    # Task 7: Generate Response
    generate_response_task = PythonOperator(
        task_id='generate_response',
        python_callable=generate_response,
        op_kwargs={
            'model': '{{ ti.xcom_pull(task_ids="load_model", key="return_value")[0] }}',
            'tokenizer': '{{ ti.xcom_pull(task_ids="load_model", key="return_value")[1] }}',
            'prompt': "Summarize the provided code solution...",
        },
    )

    # Define task dependencies
    install_deps_task >> load_packages_task >> load_model_task
    load_model_task >> configure_model_task
    load_model_task >> prepare_dataset_task
    prepare_dataset_task >> train_model_task
    load_model_task >> generate_response_task
