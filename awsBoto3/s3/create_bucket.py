import json
import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Union
from urllib import request, parse, response 
import os 

logger = logging.getLogger()
logger.setLevel(logging.INFO)


s3 = boto3.client('s3')

props = {
    'name': 'sdk-lambda-bkt'
}


def s3_bucket(region: Dict) -> Dict:
    try:
        logger.info("Creating bucket {}".format(f"{props['name']}"))
        bucket = s3.create_bucket(
            Bucket = f"{props['name']}",
            CreateBucketConfiguration = region
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            print(f"Bucket {props['name']} already exists. Name should be unique.")
            return f"{props['name']}: arn:aws:s3:::{props['name']}"
        raise err
    else:
        return bucket


def s3_list() -> List:
    try:
        buckets = s3.list_buckets()
        list_of_buckets = []
        for bucket in buckets['Buckets']:
            list_of_buckets += {bucket['Name']}
    except ClientError as err:
        logger.info("Cannot find {}".format(f"{props['name']}"))
        raise
    else:
        return list_of_buckets


def upload_file1(file_name, object_name=None, bucket=f"{props['name']}"):    
    lines = [
            '#!bin/bash',
            'sudo yum install -y git',
            'sudo yum install -y docker',
            'sudo systemctl start docker',
            'sudo yum install python3',
            'python --version',
            'sudo yum install python3-pip'
        ]
    with open('sample.sh', 'w') as object_file:
            content = object_file.write(
                '\n'.join(lines)
            )

    logger.info("Creating object {} in {} bucket.".format(file_name, bucket))

        # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

        # Upload the file
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    

if __name__=='__main__':
    print(s3_bucket(
        {
            "LocationConstraint": "ap-south-1"
        }
    ))
    print(s3_list())
    print(upload_file1("sample.sh"))