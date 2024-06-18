from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from src.model.load_model import load_model_tokeniser
from src.model.save_model import save_model
from src.model.model_eval import evaluate_model
from src.model.model_training import prepare_dataset,train_model

dag = DAG(
    'model_pipeline',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2024, 5, 8),
    },
    schedule_interval=None,
)

# Define tasks
task_load_model_tokenizer = PythonOperator(
    task_id='load_model_tokenizer',
    python_callable=load_model_tokeniser,
    provide_context=True,
    dag=dag,
)

task_prepare_dataset = PythonOperator(
    task_id='prepare_dataset',
    python_callable=prepare_dataset,
    provide_context=True,
    # input from data pipeline
    op_kwargs={'input_data': input_data},  # Pass the input data here
    dag=dag,
)

task_train_model = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    provide_context=True,
    dag=dag,
)

task_evaluate_model = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    provide_context=True,
    dag=dag,
)

task_save_model = PythonOperator(
    task_id='save_model',
    python_callable=save_model,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
task_load_model_tokenizer >> task_prepare_dataset >> task_train_model >> task_evaluate_model >> task_save_model