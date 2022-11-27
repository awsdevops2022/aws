import boto3
from botocore.exceptions import ClientError
import os
import sys

sys.path.insert(1, f'{os.getcwd()}/..')

from log_record import log

client = boto3.client('lambda')


class LambdaNew():

    def __init__(self):
        self.name = "demo-project-function"

    @log 
    def lambdaCreation(self):
        try:
            response = client.create_function(
                Code={
                    'S3Bucket': 'demo-project-bkt',
                    'S3Key': 'lambda_ec2.py.zip'
                },
                Description='To start ec2 instances when objects uploaded to s3',
                FunctionName= self.name,
                Handler='lambda_ec2.handler',
                MemorySize=256,
                Publish=True,
                Role='arn:aws:iam::12345678:role/service-role/LambdaTriggerEc2ExecRole',
                Runtime='python3.9',
                Timeout=120, #In seconds
            )
            print(response)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServiceException':
                print("The lambda function failed to create !!")
            raise e 

    @log
    def invokeLambda(self):
        try:
            response = client.invoke(
                FunctionName = self.name,
                InvocationType = 'Event'
            )
            result = response['StatusCode']
            if result == 200:
                print('Invoke is successful')
            else:
                print('Failed to invoke')
        except ClientError as error:
            if error.response["Error"]["Code"] == "EC2AccessDeniedException":
                print("Requires iam permissions to start ec2 instances")
            raise error


def main():
    lambda_new = LambdaNew()
    lambda_new.lambdaCreation()
    lambda_new.invokeLambda()

if __name__ == '__main__':
    main()