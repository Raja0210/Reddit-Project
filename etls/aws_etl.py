import s3fs
import logging
from utils.constants import AWS_ACCESS_KEY_ID,AWS_ACCESS_KEY

def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(anon=False,
                               key= AWS_ACCESS_KEY_ID,
                               secret=AWS_ACCESS_KEY)
        return s3
    except Exception as e:
        logging.error(f"Error in connect_to_s3: {str(e)}")

def create_bucket_if_not_exist(s3: s3fs.S3FileSystem, bucket:str):
    try:
        if not s3.exists(bucket):
            s3.mkdir(bucket)
            print("Bucket created")
        else:
            print("Bucket already exists")
    except Exception as e:
        logging.error(f"Error in create_bucket_if_not_exist: {str(e)}")

def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket:str, s3_file_name: str ):
    try:
         s3.put(file_path,bucket+'/raw/'+s3_file_name)
         print('File uploaded to s3')
    except Exception as e:
        logging.error(f"Error in upload_to_s3: {str(e)}")
        print(bucket+'/raw/'+s3_file_name)
        print(file_path)