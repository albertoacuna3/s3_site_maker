from os import listdir
from os.path import isfile, join, isdir, basename, splitext

import boto3
from botocore.client import ClientError


class AWSController:
    def __init__(self):
        self.s3_client = boto3.resource('s3')

    def put_directory_in_bucket(self, bucket_name, bucket_folder, dir_location, is_recursive=True):
        dir_list = [f for f in listdir(
            dir_location) ]

        for fn in dir_list:
            if isfile(join(dir_location, fn)):
                key = fn

                if bucket_folder:
                    key = join(bucket_folder, fn)

                self.upload_file_to_s3_bucket(bucket_name, join(dir_location, fn), key)

            elif isdir(join(dir_location, fn)) and is_recursive:
                if bucket_folder:
                    fn = join(bucket_folder, fn)

                print("Creating folder %s" % fn)
                self.create_bucket_folder(bucket_name, fn)

                self.put_directory_in_bucket(
                    bucket_name,
                    fn,
                    join(dir_location, basename(fn)),
                    is_recursive)


    def create_bucket_folder(self, bucket_name, folder_name):
        try:
            response = self.s3_client.Bucket(bucket_name).put_object(ACL='public-read', Body='', Key=folder_name + '/')
        except ClientError:
            print('Was unable to create the folder')
        return response

    def deploy(self, dir_location, environment):
        main_bucket = environment.get('Buckets').get('Main')
        # response = self.delete_objects_in_bucket(bucket_name)
        try:
            self.s3_client.meta.client.head_bucket(Bucket=main_bucket)
        except ClientError:
            print("Creating the bucket...")
            self.create_s3_bucket(main_bucket, 'private', {
                'LocationConstraint': 'us-west-2'})

        self.put_directory_in_bucket(main_bucket, None, dir_location, True)
        #TODO: make it optional to change the index and error files
        self.make_bucket_website(main_bucket, 'index.html', 'error.html')

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
        filename, file_extension = splitext(file_path)

        print('Uploading file %s...' % key)

        bucket.upload_file(file_path, key, ExtraArgs={
            'ACL': 'public-read', 'ContentType': self.get_file_content_type(file_extension[1:])})

    def create_s3_bucket(self, bucket_name, acl, bucket_config):
        self.s3_client.create_bucket(ACL=acl,
                                     Bucket=bucket_name,
                                     CreateBucketConfiguration=bucket_config)

    def undeploy(self, environment):
        main_bucket = environment.get('Buckets').get('Main')
        response = self.delete_objects_in_bucket(main_bucket)

    def delete_objects_in_bucket(self, bucket_name):
        print('Deleting the %s bucket...' % bucket_name)
        bucket = self.s3_client.Bucket(bucket_name)

        object_list = self.get_bucket_objects(bucket_name)
        object_list = {'Objects': [{'Key': d['Key']} for d in object_list]}

        response = bucket.delete_objects(Delete=object_list)

        return response

    def make_bucket_website(self, bucket_name, index_file, error_file):
        bucket_website = self.s3_client.BucketWebsite(bucket_name)
        print('Setting the bucket %s as a website' % bucket_name)
        bucket_website.put(
            WebsiteConfiguration={
                'ErrorDocument': {
                    'Key': error_file
                },
                'IndexDocument': {
                    'Suffix': index_file
                }
            }
        )