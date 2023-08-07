import io
import os
import argparse
import requests
import re
from urllib.request import urlopen
import json
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Union
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


@dataclass
class Config:
    AssetId: str 
    url: str = "https://www.python.org/static/img/python-logo.png" #This is python logo image.


file_str_pattern = re.compile(r'^p\w+') #It is the enforcing the pattern for creating filename.

response = Config("12345")


parser = argparse.ArgumentParser(description=("Provide the name and region for the file to be created. \n"
                                              "For help. Type 'python data__classes.py --help'. \n"
                                              "To run the script for example. Type 'python data__classes.py pylogo aps1'."
                                              ))


parser.add_argument(
        "filename",
        type=str,
        help="Name of the file must begin with 'p'. Ex-pylogo"
    )

parser.add_argument(
    "region",
    type=str,
    metavar="regionName",
    help="Provide region short name. Ex: ap-south-1 as aps1."
)

args = parser.parse_args()
input = args.filename


def format_name() -> List:
    res = re.findall(file_str_pattern, input)
    return res


def new_file_name():
    """ It formats the input filename given from
    the command line to the below format"""

    new_name = f'p{response.AssetId}-{format_name()[0]}-{args.region}.png'
    return new_name


def download_save():
    """It downloads the file/image from the internet and 
    saves it to the local(This can be the same directory or 
    any other directory path defined)"""

    a = urlopen(response.url)
    information = a.info()

    if information.get_content_type() == 'image/png':
        r = requests.get(response.url)
        b = io.BytesIO(r.content)
        print(r.status_code) #Returns 200 if successful.
        function = new_file_name()
        location = os.path.join("./python", function)
        full_path = os.path.abspath(location)
        print(full_path)

        with open(function, "wb") as file:
            file.write(b.getvalue())
        b.close()
        return function
    else:
        print("Failed to download the image")


#using s3 client
s3 = boto3.client('s3')


def buckets_list() -> List:
    """A list of buckets are returned"""

    response = s3.list_buckets()
    list_of_buckets = []
    for bucket in response['Buckets']:
        list_of_buckets.append(bucket['Name'])
    return list_of_buckets


def upload_to_s3(object_name = None):
    """Checks whether the said bucket is available in the list of buckets.
    If yes it uploads the file to the bucket.
    Make sure the bucket is available in the regions"""

    file_name = download_save()
    bucket_names = buckets_list()
    for bucket in bucket_names:
        if bucket == "sdk-lambda-bkt":
            if object_name is None:
                object_name = os.path.basename(file_name)

                # Upload the file
            try:
                response = s3.upload_file(file_name, bucket, object_name)
                print(file_name + " uploaded!!")
            except ClientError:
                print("Failed to upload file")
                return False
            return True



if __name__ == '__main__':
    upload_to_s3()