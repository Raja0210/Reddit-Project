import logging
from etls.aws_etl import connect_to_s3, create_bucket_if_not_exist, upload_to_s3
from utils.constants import AWS_BUCKET_NAME

def upload_s3_pipeline(ti):
    try:
        file_path = ti.xcom_pull(task_ids='reddit_extraction', key='return_value')

        s3 = connect_to_s3()
        create_bucket_if_not_exist(s3, AWS_BUCKET_NAME)
        upload_to_s3( , file_path, AWS_BUCKET_NAME, file_path.split('/')[-1])
    except Exception as e:
        logging.error(f"Error in upload_s3_pipeline: {str(e)}")
        raise