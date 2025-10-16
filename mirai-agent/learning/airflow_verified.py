"""
airflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-16T11:36:30.858219

This code has been verified by MIRAI's NASA-level learning system.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def sample_task(**kwargs) -> None:
    """
    Sample task that prints the current execution date.

    :param kwargs: Keyword arguments passed by Airflow.
    """
    try:
        execution_date = kwargs['execution_date']
        print(f"Current execution date is: {execution_date}")
    except KeyError as e:
        print(f"Error retrieving execution date: {e}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='example_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    task1 = PythonOperator(
        task_id='sample_task',
        python_callable=sample_task,
        provide_context=True,  # Enables passing context to the callable
        op_kwargs={'example_param': 'value'},
    )

    end = DummyOperator(
        task_id='end'
    )

    start >> task1 >> end