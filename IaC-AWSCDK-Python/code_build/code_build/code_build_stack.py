import json
from os import access
import queue
from aws_cdk import (
    Duration,
    DockerImage,
    SecretValue,
    Stack,
    aws_codebuild as codebuild,
    aws_secretsmanager as sm,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_ecr as ecr,
    RemovalPolicy,
    Aws,
    SecretValue
)

import aws_cdk
from constructs import Construct

class CodeBuildStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        props = {'namespace': 'cdk-example-codebuild'}


        #role = iam.Role(self, "githubCredRole", assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"), description="Role created for codebuild to use secretmanager")

        vpc = ec2.Vpc(self, "cdkVpc", cidr="192.0.0.0/16", enable_dns_hostnames=True, enable_dns_support=True, nat_gateways=0, availability_zones=["ap-south-1a"],
                subnet_configuration=[ec2.SubnetConfiguration(name="cdk-public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24)])

        securityGroup = ec2.SecurityGroup(self, "cdkSecurityGroup", vpc=vpc, description="cdk security group", security_group_name="cdk-instance-securitygroup")

        securityGroup_ingress = securityGroup.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.all_traffic(),
            description="allow SSH access from anywhere on port 22"
        )

        
        elastic_container_registry = ecr.Repository(
            self, "ECR",
            repository_name=f"{props['namespace']}",
            removal_policy=RemovalPolicy.DESTROY
        )


        git_hub_creds = codebuild.GitHubSourceCredentials(self, "CodeBuildGitCreds", access_token=SecretValue.secrets_manager(
            secret_id="githubCred",
            json_field="Token"
        ))
        
        git_hub_source=codebuild.Source.git_hub(
            owner="awsdevops2022",
            repo="aws",
            branch_or_ref="development",
            webhook=True
        )

        build = codebuild.BuildSpec.from_source_filename(
            filename="dockerImage/docker_image_buildspec.yml"
        )

        build_environment = codebuild.BuildEnvironment(
            build_image=codebuild.LinuxBuildImage.STANDARD_4_0,
            compute_type=codebuild.ComputeType.SMALL,
            environment_variables={
                'ecr': codebuild.BuildEnvironmentVariable(value=ecr.Repository.repository_uri),
                'tag': codebuild.BuildEnvironmentVariable(value="cdk"),
                'region': codebuild.BuildEnvironmentVariable(value=Aws.REGION),

            },
            privileged=True
        )

        project = codebuild.Project(
            self,
            "cdk-code-build",
            source=git_hub_source,
            build_spec=build,
            description="codebuild project using AWS Cdk",
            logging=codebuild.LoggingOptions(
                cloud_watch=codebuild.CloudWatchLoggingOptions(
                    log_group=logs.LogGroup(self, "cdkLogGroup")
                )
            ),
            security_groups=[securityGroup],
            vpc=vpc,
            queued_timeout=aws_cdk.Duration.minutes(15),
            timeout=aws_cdk.Duration.minutes(15)
        )