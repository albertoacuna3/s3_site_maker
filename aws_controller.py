import os
import boto3
import json
from os import listdir, getcwd
from os.path import isfile, join


class AWSController:
    def __init__(self):
        self.s3_client = boto3.resource('s3')

    def put_directory_in_bucket(self, dir_location, bucket_name):
        files_only = [f for f in listdir(
            dir_location) if isfile(join(dir_location, f))]

        for fn in files_only:
            file_path = os.path.join(dir_location, fn)

            self.upload_file_to_s3_bucket(bucket_name, file_path, fn)

    def get_file_content_type(self, filename_ext):
        mimetypes = {
            'html': 'text/html',
            'json': 'application/json',
            'css': 'text/css',
            'other': 'text/plain'
        }

        return mimetypes.get(filename_ext, mimetypes.get('other'))
    
    #TODO: Needs to be updated
    def get_bucket_objects(self, bucket_name):
        response = self.s3_client.meta.client.list_objects(
            Bucket=bucket_name
        )
        contents = response['Contents']
        formatted_contents = [{'Key': d['Key'], 'Size': d['Size'],
                               'LastModified': d['LastModified'].strftime("%B %d, %Y")} for d in contents]
        return formatted_contents

    def upload_file_to_s3_bucket(self, bucket_name, file_path, key):
        bucket = self.s3_client.Bucket(bucket_name)
        filename, file_extension = os.path.splitext(file_path)

        bucket.upload_file(file_path, key, ExtraArgs={
            'ACL': 'public-read', 'ContentType': self.get_file_content_type(file_extension[1:])})

