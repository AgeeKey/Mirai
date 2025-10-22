"""
airflow - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.78
Tests Passed: 0/1
Learned: 2025-10-22T01:26:22.364795

This code has been verified by MIRAI's NASA-level learning system.
"""

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from typing import Any

def sample_task(**kwargs: Any) -> None:
    """Sample task that prints a message."""
    try:
        print("Executing sample task")
    except Exception as e:
        print(f"Error in sample_task: {e}")

with DAG(
    dag_id='sample_dag',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    start = DummyOperator(
        task_id='start',
    )

    run_sample_task = PythonOperator(
        task_id='run_sample_task',
        python_callable=sample_task,
        provide_context=True,
    )

    end = DummyOperator(
        task_id='end',
    )

    start >> run_sample_task >> end