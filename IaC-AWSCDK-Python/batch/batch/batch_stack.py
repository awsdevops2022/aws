from distutils import command
from aws_cdk import (
    RemovalPolicy,
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_batch_alpha as batch,
    aws_ecs as ecs,
    Tags
)
from constructs import Construct

class BatchStack(Stack):

    cidr_range = "10.0.0.0/16"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        props = {'name': 'cdk-batch', 'keyPair': 'AWSDevops'}

        #vpc

        vpc = ec2.Vpc(self, "cdkBatchVpc", cidr=self.cidr_range, enable_dns_hostnames=True, enable_dns_support=True, nat_gateways=0, availability_zones=["ap-south-1a", "ap-south-1b"],
                subnet_configuration=[ec2.SubnetConfiguration(name=f"{props['name']}-public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24)])


        Tags.of(vpc).add("Environment", "Dev")
        Tags.of(vpc).add("Owner", "saikrishna")


        securityGroup = ec2.SecurityGroup(self, "cdkSecurityGroup", vpc=vpc, description="cdk batch security group", security_group_name=f"{props['name']}-security")

        Tags.of(securityGroup).add("Environment", "Dev")
        Tags.of(securityGroup).add("Owner", "saikrishna")


        securityGroup_ingress = securityGroup.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.all_traffic(),
            description="allow SSH access from anywhere on port 22"
        )


        #Job Definition

        batch_job_def = batch.JobDefinition(
            self, "batchJobDef", 
            container=batch.JobDefinitionContainer(
                image=ecs.ContainerImage.from_registry(
                    "public.ecr.aws/amazonlinux/amazonlinux:latest"
                ),
                command=["echo", "Hello World !!"],
                memory_limit_mib=512,
                privileged=True,
                read_only=False,
                vcpus=1
            ),
            job_definition_name=f"{props['name']}-job",
            platform_capabilities=[batch.PlatformCapabilities("EC2")],
            retry_attempts=1,
        )

        Tags.of(batch_job_def).add("Environment", "Dev")
        Tags.of(batch_job_def).add("Owner", "saikrishna")


        #compute Environment

        batch_env = batch.ComputeEnvironment(
            self, "cdkCompEnv",
            compute_environment_name=f"{props['name']}-env",
            compute_resources=batch.ComputeResources(
                vpc=vpc,
                ec2_key_pair=f"{props['keyPair']}",
                minv_cpus=1,
                desiredv_cpus=2,
            )
        )
        
        Tags.of(batch_env).add("Environment", "Dev")
        Tags.of(batch_env).add("Owner", "saikrishna")

        #job queue

        batch_queue = batch.JobQueue(
            self,"cdkJobQueue",
            compute_environments=[
                batch.JobQueueComputeEnvironment(
                    compute_environment=batch_env,
                    order=1
                )
            ],
            job_queue_name=f"{props['name']}-queue",
            priority=1
        )
        
        Tags.of(batch_queue).add("Environment", "Dev")
        Tags.of(batch_queue).add("Owner", "saikrishna")


        #removal policy of job definition after deletion

        remove_job_def = batch_job_def.apply_removal_policy(RemovalPolicy.DESTROY)
        
        #output resources

        CfnOutput(self, "BatchJobQueue", value=batch_queue.job_queue_name)
        CfnOutput(self, "JobDefinition", value=batch_job_def.job_definition_name)