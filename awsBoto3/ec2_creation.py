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
    'subnet_cidr': '192.0.0.0/24',
    'prefix': 'sdk-',
    'image-id': 'ami-06489866022e12a14',
    'instance-type': ['t2.micro', 't2.medium']
} 

client = boto3.client("ec2", region_name= f"{props['region']}")


def create_new_vpc():
    """Defining a custom vpc"""
    try:
        vpc = client.create_vpc(
            CidrBlock = f"{props['cidr']}",
            TagSpecifications = [
                {
                    "ResourceType": "vpc",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": f"{props['prefix']}vpc"
                        }
                    ]
                }
            ]
        )
    except ClientError:
        logger.exception("Couldn't create vpc")
        raise
    else:
        return vpc



def main():    
    """ 
    This creates vpc, subnet, internet gateway and attaches the internet gateway to Vpc. 
    We are calling the above function to extract the VpcId and attaches subnet to it, modifying subnet attributes. 
    Similarly, we are attaching the internet gateway id.
    We're creating route table, associating route table to subnet, creating route.
    Creating security groups with ingress and egress rules.
    Creating an instance.
    """

    try:
        calling_vpc = create_new_vpc()
        subnet = client.create_subnet(
            TagSpecifications = [
                {
                    "ResourceType": "subnet",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": f"{props['prefix']}subnet" 
                        }
                    ]
                }
            ],
            AvailabilityZone = f"{props['az'][0]}",
            CidrBlock = f"{props['subnet_cidr']}",
            VpcId = calling_vpc['Vpc']['VpcId']
        )
    except ClientError:
        logger.exception("Couldn't create subnet")
        raise
    try:
        modify_subnet = client.modify_subnet_attribute(
            MapPublicIpOnLaunch = {
                'Value': True
            },
            SubnetId = subnet['Subnet']['SubnetId'],
        )
    except ClientError:
        logger.exception('Failed to modify attributes of subnet')
        raise


    try:
        igw = client.create_internet_gateway(
                TagSpecifications = [
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f"{props['prefix']}igw"
                        },
                    ]
                },
            ],
        )
    except ClientError:
        logger.exception('Failed to create internet gateway')
        raise


    try: 
        attach_igw = client.attach_internet_gateway(
            InternetGatewayId = igw['InternetGateway']['InternetGatewayId'],
            VpcId = calling_vpc['Vpc']['VpcId']
        )
    except ClientError:
        logger.exception('Failed to attach internet gateway')
        raise
    

    try:
        route_table = client.create_route_table(
                    VpcId = calling_vpc['Vpc']['VpcId'],
                    TagSpecifications = [
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': f"{props['prefix']}rtb"
                            },
                        ]
                    },
                ],
            )
    except ClientError:
        logger.exception('Failed to create route table')
        raise

    try:
        associate_rtb = client.associate_route_table(
            RouteTableId = route_table['RouteTable']['RouteTableId'],
            SubnetId = subnet['Subnet']['SubnetId'],
        )
    except ClientError:
        logger.exception('Failed to associate route')
        raise
    except IndexError:
        logger.exception('list index out of range. Need to filter data properly')
        raise 

    
    try:
        route = client.create_route(
            DestinationCidrBlock = '0.0.0.0/0',
            GatewayId = igw['InternetGateway']['InternetGatewayId'],
            RouteTableId = route_table['RouteTable']['RouteTableId']
        )
    except ClientError:
        logger.exception('Failed to route')
        raise


    try:
        security_group = client.create_security_group(
            Description = 'Security group',
            GroupName = f"{props['prefix']}secgrp",
            VpcId = calling_vpc['Vpc']['VpcId'],
            TagSpecifications = [
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f"{props['prefix']}secgrp"
                        }
                    ]
                }
            ]
        )
    except ClientError:
        logger.exception('Failed to route')
        raise
    

    try:
        secgrp_ingress = client.authorize_security_group_ingress(
            GroupId = security_group['GroupId'],
            IpPermissions=[
                {
                    'FromPort': 22,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                            'Description': 'SSH access from anywhere',
                        },
                    ],
                    'ToPort': 22,
                },
                {
                    'FromPort': 8080,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                            'Description': 'port 8080 access from anywhere',
                        }
                    ],
                    'ToPort': 8080
                }
            ],
        )
        secgrp_egress = client.authorize_security_group_egress(
            GroupId = security_group['GroupId'],
            IpPermissions=[
                {
                    'FromPort': 8080,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                            'Description': 'port 8080 to anywhere',
                        },
                    ],
                    'ToPort': 8080,
                },
            ],
        )
    except ClientError:
        logger.exception('Failed to segurity group rules')
        raise


    try:
        create_instance = client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdh',
                    'Ebs': {
                        'VolumeSize': 20,
                    },
                },
            ],
            ImageId = f"{props['image-id']}",
            InstanceType = f"{props['instance-type'][0]}",
            KeyName = 'AWSDevops',
            MaxCount = 1,
            MinCount = 1,
            SecurityGroupIds=[
                security_group['GroupId'],
            ],
            SubnetId = subnet['Subnet']['SubnetId'],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f"{props['prefix']}dev",
                        },
                    ],
                },    
            ],
        )
    except ClientError:
        logger.exception('Failed to create instance')
        raise

    else:
        return subnet, igw, attach_igw, route_table, route, associate_rtb, security_group, secgrp_ingress, secgrp_egress, create_instance, modify_subnet
 
        

if __name__ == '__main__':
    logger.info("Creating a custom vpc and subnet...")
    main()