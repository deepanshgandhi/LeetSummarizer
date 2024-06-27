import datetime

import airflow
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.google.cloud.hooks.compute_ssh import ComputeEngineSSHHook

GCE_INSTANCE = 'leetummarizer'
GCE_ZONE = 'us-west4-a'
GCP_PROJECT_ID = 'leetsummarizer'

with airflow.DAG(
        'composer_compute_ssh_dag',
        start_date=datetime.datetime(2022, 1, 1)
        ) as dag:

  ssh_task = SSHOperator(
      task_id='composer_compute_ssh_task',
      ssh_hook=ComputeEngineSSHHook(
          instance_name=GCE_INSTANCE,
          zone=GCE_ZONE,
          project_id=GCP_PROJECT_ID,
          use_oslogin=True,
          use_iap_tunnel=False,
          use_internal_ip=True),
      command='echo This command is executed from a DAG',
      dag=dag)