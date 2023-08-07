import boto3
import argparse
from botocore.exceptions import ClientError


s3 = boto3.client('s3')

parser = argparse.ArgumentParser(description=("Provide the region where bucket will be created. \n"
                                              "For help. Type 'python s3.py --help'. \n"
                                              "To run the script for example. Type 'python s3.py ap-south-1'"
                                              ))


parser.add_argument(
    "region",
    type=str,
    metavar="regionName",
    help="Provide region full name. Ex: ap-south-1, us-east-1."
)

args = parser.parse_args()
input_region = args.region


class Bucket():

    bucket = "demo-project-bkt"

    def __init__(self, input_region):
        self.input_region = input_region


    def bucket_create(self):
        try:
            location = {'LocationConstraint': self.input_region}
            response = s3.create_bucket(Bucket = self.bucket, CreateBucketConfiguration = location)
        except ClientError as error:
            if error.response["Error"]["Code"] == "BucketAlreadyExists":
                print("Bucket already exists !!")
            raise error    


    def listing_buckets(self):
        response = s3.list_buckets()
        list_of_buckets = []
        for bucket in response['Buckets']:
            list_of_buckets.append(bucket['Name'])
        print(f"The list of buckets are: {list_of_buckets}")
        

def main():
    bkt = Bucket(input_region)
    bkt.bucket_create()
    bkt.listing_buckets()

if __name__ == '__main__':
    main()
