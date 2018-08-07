import os
import boto3
import json

#TODO:Have to double check how I want to do credentials
s3 = boto3.resource('s3')

def get_bucket_objects(bucket):
    response =  s3.meta.client.list_objects(
        Bucket=bucket
    )

    if response:
        return response['Contents']

def get_current_directory():
    return os.getcwd()

def push_files_to_s3(filename, bucket, filename_key):
    #TODO: Load files to S3
    s3.meta.client.upload_file(filename, bucket, filename_key)

def load_config_file():
    #TODO: Read a config file. Currently only check current directory
    with open('aws_site_maker.json') as f:
        config = json.load(f)

    return config

config_file = load_config_file()
contents = get_bucket_objects(config_file['BucketName'])

print(contents)
