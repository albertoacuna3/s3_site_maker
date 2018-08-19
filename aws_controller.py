import os
import boto3
import json
from os import listdir, getcwd
from os.path import isfile, join, isdir
from botocore.client import ClientError


class AWSController:
    def __init__(self):
        self.s3_client = boto3.resource('s3')

    def put_directory_in_bucket(self, dir_location, bucket_name, is_recursive=False):
        files_only = [f for f in listdir(
            dir_location) if isfile(join(dir_location, f))]

        child_directories = [f for f in listdir(
            dir_location) if isdir(join(dir_location, f))]

        if is_recursive:
            # TODO: Make this recursive
            pass

        for fn in files_only:
            file_path = os.path.join(dir_location, fn)

            self.upload_file_to_s3_bucket(bucket_name, file_path, fn)

    def deploy(self, dir_location, environment):
        main_bucket = environment.get('Buckets').get('Main')
        # response = self.delete_objects_in_bucket(bucket_name)
        try:
            self.s3_client.meta.client.head_bucket(Bucket=main_bucket)
        except ClientError:
            print("Creating the bucket...")
            self.create_s3_bucket(main_bucket, 'private', {
                'LocationConstraint': 'us-west-2'})

        self.put_directory_in_bucket(dir_location, main_bucket, False)

    def get_file_content_type(self, filename_ext):
        mimetypes = {
            'html': 'text/html',
            'json': 'application/json',
            'css': 'text/css',
            'other': 'text/plain'
        }

        return mimetypes.get(filename_ext, mimetypes.get('other'))

    # TODO: Needs to be updated
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

    def create_s3_bucket(self, bucket_name, acl, bucket_config):
        self.s3_client.create_bucket(ACL=acl,
                                     Bucket=bucket_name,
                                     CreateBucketConfiguration=bucket_config)

    def undeploy(self, environment):
        for bucket_name in environment.get('Buckets'):
            response = self.delete_objects_in_bucket(bucket_name)

    def delete_objects_in_bucket(self, bucket_name):
        bucket = self.s3_client.Bucket(bucket_name)

        object_list = self.get_bucket_objects(bucket_name)
        object_list = {'Objects': [{'Key': d['Key']} for d in object_list]}

        response = bucket.delete_objects(Delete=object_list)

        return response
