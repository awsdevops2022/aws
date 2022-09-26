import json
import logging
from typing import Dict, List, Union
import boto3
from botocore.exceptions import ClientError

client = boto3.client("iam")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)

policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*"
            ],
            "Resource": "*"
        }
    ]
}


def s3_readonly_policy(name: str, description: str, tags: List, policy_document: Dict, path: str = "/") -> Dict:

    print(f"Creating {name} policy...")
    try:
        logger.info("Starting")
        s3_read_only = client.create_policy(
            PolicyName = name,
            Path = path,
            PolicyDocument = json.dumps(policy_document, indent=4),
            Description = description,
            Tags = tags
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "EntityAlreadyExists":
            print(f"WARNING: Policy {name} already exists")
            return f"arn:aws:iam::aws:policy/{name}"
        else:
            raise err
    arn = s3_read_only['Policy']['Arn']
    print(f"IAM policy {name} with {arn} created")
    return arn 


if __name__=='__main__':
    s3_readonly_policy(
        "sdk-s3",
        "To create a s3 read only access policy using sdk",
        [
            {
                "Key": "Name",
                "Value": "sdk-s3-read-only"
            }
        ],
        policy_document  
    )