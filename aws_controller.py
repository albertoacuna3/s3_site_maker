import os
import boto3
import json
from os import listdir, getcwd
from os.path import isfile, join


class AWSController:
    def __init__(self, location):
        self.location = location
        self.s3 = boto3.resource('s3')
        self.load_config_file()
        self.load_s3_bucket_object()

    def load_s3_bucket_object(self):
        if self.config_file is None:
            self.load_config_file()

        self.s3_bucket = self.s3.Bucket(self.config_file['BucketName'])

    def put_directory_in_bucket(self, location):
        if self.s3_bucket is None:
            self.load_s3_bucket_object()

        files_only = [f for f in listdir(
            location) if isfile(join(location, f))]

        for fn in files_only:
            file_path = os.path.join(self.location, fn)

            self.push_file_to_s3(file_path, fn)

    def get_file_content_type(self, filename_ext):
        mimetypes = {
            'html': 'text/html',
            'json': 'application/json',
            'css': 'text/css',
            'other': 'text/plain'
        }

        return mimetypes.get(filename_ext, mimetypes.get('other'))

    def get_bucket_objects(self, bucket):
        response = self.s3.meta.client.list_objects(
            Bucket=bucket
        )
        contents = response['Contents']
        formatted_contents = [{'Key': d['Key'], 'Size': d['Size'],
                               'LastModified': d['LastModified'].strftime("%B %d, %Y")} for d in contents]
        return formatted_contents

    def push_file_to_s3(self, file_path, filename_key):
        filename, file_extension = os.path.splitext(file_path)
        self.s3_bucket.upload_file(file_path, filename_key, ExtraArgs={
            'ACL': 'public-read', 'ContentType': self.get_file_content_type(file_extension[1:])})

    def load_config_file(self):
        config_file = join(self.location, 'aws_site_maker.json')
        with open(config_file) as f:
            self.config_file = json.load(f)
