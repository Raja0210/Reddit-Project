from airflow import DAG
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from airflow.operators.python import PythonOperator
from pipelines.reddit_pipeline import reddit_extraction
from pipelines.aws_s3_pipeline import upload_s3_pipeline

default_args={
    'owner': 'Raja',
    'start_date': datetime(2024, 3,15),
    'email': 'rajagopalanr0210@gmail.com',
    'email_on_failure': True,
    'email_on_retry': True,
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag=DAG(
    dag_id='reddit_dag',
    description='etl_reddit_pipeline',
    default_args=default_args,
    max_active_runs=1,
    catchup=False,
    schedule_interval='@daily'
)

extract_reddit = PythonOperator(
    task_id='reddit_extraction',
    python_callable=reddit_extraction,
    op_kwargs={
        'file_name': f'reddit_{file_postfix}',
        'subreddit': 'dataengineering',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

upload_s3 = PythonOperator(
    task_id= 's3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)

extract_reddit >> upload_s3