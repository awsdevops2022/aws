from urllib import response
import boto3
import logging
from botocore.exceptions import ClientError
import json

logger = logging.getLogger(__name__)

props = {
    'region': 'ap-south-1',
    'cidr': '192.0.0.0/16',
    'az': ["ap-south-1a", "us-east-1a"],
    'subnet_cidr': '192.0.0.0/24'
} 

ec2 = boto3.client("ec2", region_name= f"{props['region']}")

def main():
    try:
        vpc = ec2.create_vpc(
            CidrBlock = f"{props['cidr']}",
            TagSpecifications = [
                {
                    "ResourceType": "vpc",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "sdk-vpc"
                        }
                    ]
                }
            ]
        )
        subnet = ec2.create_subnet(
            TagSpecifications = [
                {
                    "ResourceType": "subnet",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "sdk-subnet" 
                        }
                    ]
                }
            ],
            AvailabilityZone = f"{props['az'][0]}",
            CidrBlock = f"{props['subnet_cidr']}",
            VpcId = vpc['Vpc']['VpcId']
        )
    except ClientError:
        logger.exception("Couldn't create vpc")
        logger.exception("Couldn't create subnet")
        raise
    else:
        return vpc, subnet 



def get_available_vpcs():
    details_vpc = ec2.describe_vpcs(
        Filters =  [
            {
                'Name': 'vpc-id',
                'Values': ['available']
            },
        ],
    ).get('Vpcs')
    for details in details_vpc:
        info = details['VpcId']
        print([f"{info}"])
    

if __name__ == '__main__':
    logger.info("Creating a custom vpc and subnet...")
    custom_vpc = main()
    print(custom_vpc)
    print(get_available_vpcs())

