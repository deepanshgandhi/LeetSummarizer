# Import necessary libraries and modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
#from src.data_preprocessing.handle_comments import remove_comments
from airflow import configuration as conf


from src.data_preprocessing.load_data import load_data
from src.data_preprocessing.handle_comments import remove_comments
# from src.data_preprocessing.validate_code import  validate_code
# from src.data_preprocessing.validate_schema import validate_schema

conf.set('core', 'enable_xcom_pickling', 'True')

default_args = {
    'owner': 'brijesh',
    'start_date': datetime(2024, 5, 18),
    'retries': 0,  # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5),  # Delay before retries
}


dag = DAG(
    'data_pipline_v2',
    default_args=default_args,
    description='Your Python DAG Description',
    schedule_interval=None,  # Set the schedule interval or use None for manual triggering
    catchup=False,
)


# load_data_task = PythonOperator(
#     task_id='load_data_task',
#     python_callable=load_data,
#     dag=dag,
# )


# data_preprocessing_task = PythonOperator(
#     task_id='data_preprocessing_task',
#     python_callable=data_preprocessing,
#     op_args=[load_data_task.output],
#     dag=dag,
# )


# build_save_model_task = PythonOperator(
#     task_id='build_save_model_task',
#     python_callable=build_save_model,
#     op_args=[data_preprocessing_task.output, "model2.sav"],
#     provide_context=True,
#     dag=dag,
# )



# load_model_task = PythonOperator(
#     task_id='load_model_task',
#     python_callable=load_model_elbow,
#     op_args=["model2.sav", build_save_model_task.output],
#     dag=dag,
# )










task_load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)
# # Define the tasks
task_handle_comments = PythonOperator(
    task_id='handle_comments',
    python_callable=remove_comments,
    op_args=[task_load_data.output],
    dag=dag,
)

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

# # Define the test tasks using BashOperator to run your test scripts
# task_test_remove_comments = BashOperator(
#     task_id='test_remove_comments',
#     bash_command='pytest tests/test_remove_comments.py',
#     dag=dag,
# )

# task_test_validate_code = BashOperator(
#     task_id='test_validate_code',
#     bash_command='pytest tests/test_validate_code.py',
#     dag=dag,
# )

# Define task dependencies
# task_handle_comments >> task_validate_code >> task_validate_schema
# task_handle_comments >> task_test_remove_comments
# task_validate_code >> task_test_validate_code

task_load_data 
# load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task



if __name__ == "__main__":
    dag.cli()