from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2
)


from constructs import Construct

class Ec2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        vpc = ec2.Vpc(self, "cdkVpc", cidr="192.0.0.0/16", enable_dns_hostnames=True, enable_dns_support=True, nat_gateways=0, availability_zones=["ap-south-1a"],
                subnet_configuration=[ec2.SubnetConfiguration(name="cdk-public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24)])

        securityGroup = ec2.SecurityGroup(self, "cdkSecurityGroup", vpc=vpc, description="cdk security group", security_group_name="cdk-instance-securitygroup")

        securityGroup_ingress = securityGroup.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="allow SSH access from anywhere on port 22"
        )

        instanceType = ec2.InstanceType.of(
            ec2.InstanceClass.T2,
            ec2.InstanceSize.MICRO
        )

        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            cpu_type=ec2.AmazonLinuxCpuType.X86_64, 
            virtualization=ec2.AmazonLinuxVirt.HVM, 
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        instance = ec2.Instance(
            self,
            "cdk_instance",
            instance_type=instanceType,
            machine_image=amzn_linux,
            vpc=vpc,
            security_group=securityGroup,
            key_name="AWSDevops"
        )
