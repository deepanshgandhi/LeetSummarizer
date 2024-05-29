from airflow import DAG 
from airflow.operators.python_operator import PythonOperator  # type: ignore
from datetime import datetime, timedelta 

from Model_func import install_packages, login_huggingface, load_data, preprocess_data, load_model_and_tokenizer, configure_peft, create_training_arguments, train_model, save_model, load_trained_model, generate_text # type: ignore

def task_install_packages():
    install_packages()

def task_login_huggingface():
    login_huggingface("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")

def task_load_data(**kwargs):
    train_df = load_data('train.xlsx')
    test_df = load_data('test.xlsx')
    kwargs['ti'].xcom_push(key='train_df', value=train_df)
    kwargs['ti'].xcom_push(key='test_df', value=test_df)

def task_preprocess_data(**kwargs):
    train_df = kwargs['ti'].xcom_pull(key='train_df', task_ids='load_data')
    dataset = preprocess_data(train_df)
    kwargs['ti'].xcom_push(key='dataset', value=dataset)

def task_load_model_and_tokenizer(**kwargs):
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    model, tokenizer = load_model_and_tokenizer(model_name)
    kwargs['ti'].xcom_push(key='model', value=model)
    kwargs['ti'].xcom_push(key='tokenizer', value=tokenizer)

def task_configure_peft(**kwargs):
    peft_config = configure_peft()
    kwargs['ti'].xcom_push(key='peft_config', value=peft_config)

def task_create_training_arguments(**kwargs):
    training_arguments = create_training_arguments()
    kwargs['ti'].xcom_push(key='training_arguments', value=training_arguments)

def task_train_model(**kwargs):
    model = kwargs['ti'].xcom_pull(key='model', task_ids='load_model_and_tokenizer')
    dataset = kwargs['ti'].xcom_pull(key='dataset', task_ids='preprocess_data')
    peft_config = kwargs['ti'].xcom_pull(key='peft_config', task_ids='configure_peft')
    tokenizer = kwargs['ti'].xcom_pull(key='tokenizer', task_ids='load_model_and_tokenizer')
    training_arguments = kwargs['ti'].xcom_pull(key='training_arguments', task_ids='create_training_arguments')
    trainer = train_model(model, dataset, peft_config, tokenizer, training_arguments)
    kwargs['ti'].xcom_push(key='trainer', value=trainer)

def task_save_model(**kwargs):
    trainer = kwargs['ti'].xcom_pull(key='trainer', task_ids='train_model')
    save_model(trainer)

def task_load_trained_model(**kwargs):
    model = kwargs['ti'].xcom_pull(key='model', task_ids='load_model_and_tokenizer')
    model = load_trained_model(model)
    kwargs['ti'].xcom_push(key='trained_model', value=model)

def task_generate_text(**kwargs):
    model = kwargs['ti'].xcom_pull(key='trained_model', task_ids='load_trained_model')
    tokenizer = kwargs['ti'].xcom_pull(key='tokenizer', task_ids='load_model_and_tokenizer')
    test_df = kwargs['ti'].xcom_pull(key='test_df', task_ids='load_data')
    generate_text(model, tokenizer, test_df)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'llm_pipeline',
    default_args=default_args,
    description='Model pipeline DAG',
    schedule_interval=timedelta(days=1),
)

install_packages = PythonOperator(
    task_id='install_packages',
    python_callable=task_install_packages,
    dag=dag,
)

login_huggingface = PythonOperator(
    task_id='login_huggingface',
    python_callable=task_login_huggingface,
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=task_load_data,
    provide_context=True,
    dag=dag,
)

preprocess_data = PythonOperator(
    task_id='preprocess_data',
    python_callable=task_preprocess_data,
    provide_context=True,
    dag=dag,
)

load_model_and_tokenizer = PythonOperator(
    task_id='load_model_and_tokenizer',
    python_callable=task_load_model_and_tokenizer,
    provide_context=True,
    dag=dag,
)

configure_peft = PythonOperator(
    task_id='configure_peft',
    python_callable=task_configure_peft,
    provide_context=True,
    dag=dag,
)

create_training_arguments = PythonOperator(
    task_id='create_training_arguments',
    python_callable=task_create_training_arguments,
    provide_context=True,
    dag=dag,
)

train_model = PythonOperator(
    task_id='train_model',
    python_callable=task_train_model,
    provide_context=True,
    dag=dag,
)

save_model = PythonOperator(
    task_id='save_model',
    python_callable=task_save_model,
    provide_context=True,
    dag=dag,
)

load_trained_model = PythonOperator(
    task_id='load_trained_model',
    python_callable=task_load_trained_model,
    provide_context=True,
    dag=dag,
)

generate_text = PythonOperator(
    task_id='generate_text',
    python_callable=task_generate_text,
    provide_context=True,
    dag=dag,
)

# Define the task dependencies
install_packages >> login_huggingface >> load_data >> preprocess_data >> load_model_and_tokenizer
load_model_and_tokenizer >> configure_peft >> create_training_arguments >> train_model >> save_model >> load_trained_model >> generate_text
