import boto3
from botocore.exceptions import ClientError
import os


BASE_DIR = "/mnt/shared/mytest"

def lambda_handler(event, context):
    """
    Default lambda handler to copy from S3 bucket object to mounted efs volume
    """
    try:
        os.mkdir(BASE_DIR)
        s3 = boto3.resource('s3')
        bucket_name = "mytestbucket-989234"
        obj = "dev/mytest.txt"
        filename = "/tmp/mytest.txt"
        s3.meta.client.download_file(bucket_name, obj, filename)
    except FileExistsError:
        print(f"directory with {BASE_DIR} exists as mounted")
        pass
    except ClientError as ce:
        raise Exception(f"boto3 client error encountered.")
