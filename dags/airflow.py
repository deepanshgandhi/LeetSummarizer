# Import necessary libraries and modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.main import load_data, data_preprocessing, build_save_model, load_model_elbow
#from src.data_preprocessing.handle_comments import remove_comments
from airflow import configuration as conf

conf.set('core', 'enable_xcom_pickling', 'True')

default_args = {
    'owner': 'brijesh',
    'start_date': datetime(2024, 5, 18),
    'retries': 0,  # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5),  # Delay before retries
}


dag = DAG(
    'data_pipline_v1',
    default_args=default_args,
    description='Your Python DAG Description',
    schedule_interval=None,  # Set the schedule interval or use None for manual triggering
    catchup=False,
)


load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    dag=dag,
)


data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)


build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_save_model,
    op_args=[data_preprocessing_task.output, "model2.sav"],
    provide_context=True,
    dag=dag,
)



load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_elbow,
    op_args=["model2.sav", build_save_model_task.output],
    dag=dag,
)



# handle_comment = PythonOperator(
#     task_id='handle_comments',
#     python_callable=remove_comments,
#     op_args=[],
#     dag=dag,
# )

load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task



if __name__ == "__main__":
    dag.cli()