import boto3
import logging
import json
import urllib.parse
import argparse

s3 = boto3.client('s3')

ec2 = boto3.client('ec2')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description=("Provide the instance id to start. \n"
                                              "For help. Type 'python s3.py --help'. \n"
                                              "To run the script for example. Type 'python s3.py ap-south-1'"
                                              ))


parser.add_argument(
    "InstanceId",
    type=str,
    metavar="Instance Name",
    help="Provide region full name. Ex: ap-south-1, us-east-1."
)

args = parser.parse_args()
instance_id = args.InstanceId


def list_instances():
    stopped_instances = ec2.describe_instances(
        Filters = [{
            "Name": "instance-state-name",
            "Values": ["stopped"]
        }],
    )
    response = stopped_instances['Reservations']
    instance_list = []
    for i in response:
        res = i['Instances'][0]['InstanceId']
        instance_list.append(res)
    return instance_list


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=4))
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    if bucket == "demo-project-bkt" and key == "ec2_launch_config.sh":
        try:
            logging.info('Getting object info')
            response = s3.get_object(Bucket = bucket, Key = key)
            print("CONTENT TYPE: " + response['ContentType'])
            logging.info('Loading Instance initialization...')
            instances = list_instances()
            id = instance_id
            if id in instances:
                print('Starting InstanceId: {}'.format(id))
                start_inst = ec2.start_instances(
                    InstanceIds = [id],
                )
                state_name = start_inst['StartingInstances'][0]['CurrentState']['Name']
                print(state_name)
            else:
                print("The requested InstanceId {} does not exist or is not in stopped state.".format(id))
            return response['ContentType']
        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
            raise e
    else:
        print("Make sure the {} and {} are correct.".format(bucket, key))

