import os
import boto3
import json
from os import listdir, getcwd
from os.path import isfile, join

#TODO:Have to double check how I want to do credentials
s3 = boto3.resource('s3')
s3_bucket = None
config_file = None

def load_s3_bucket_object():
    global s3_bucket

    if config_file is None:
        load_config_file()

    s3_bucket = s3.Bucket(config_file['BucketName'])

def put_directory_in_bucket():
    global s3_bucket

    if s3_bucket is None:
        load_s3_bucket_object()

    current_path = getcwd()
    files_only = [f for f in listdir(current_path) if isfile(join(current_path, f))]

    for fn in files_only:
        filename, file_extension = os.path.splitext(fn)
        s3_bucket.upload_file(fn, fn, ExtraArgs={'ACL':'public-read', 'ContentType':get_file_content_type(file_extension[1:])})

def get_file_content_type(filename_ext):
    mimetypes = {
       'html': 'text/html',
       'json': 'application/json',
       'css': 'text/css',
       'other': 'text/plain'
    }

    return mimetypes.get(filename_ext, mimetypes.get('other'))

def get_bucket_objects(bucket):
    response =  s3.meta.client.list_objects(
        Bucket=bucket
    )
    contents =response['Contents']
    formatted_contents = [{'Key': d['Key'], 'Size': d['Size'], 'LastModified': d['LastModified'].strftime("%B %d, %Y")} for d in contents]
    return formatted_contents

def get_current_directory():
    return os.getcwd()

def push_files_to_s3(filename, bucket, filename_key):
    #TODO: Load files to S3
    s3.meta.client.upload_file(filename, bucket, filename_key)

def load_config_file():
    #TODO: Read a config file. Currently only check current directory
    global config_file
    with open('aws_site_maker.json') as f:
        config_file = json.load(f)


load_config_file()

put_directory_in_bucket()
#contents = get_bucket_objects(config_file['BucketName'])

#print(contents)
