from os import listdir
from os.path import isfile, join, isdir, basename, splitext
import sys
import boto3
from botocore.client import ClientError


class AWSController:
    def __init__(self):
        self.s3_client = boto3.resource('s3')

    def put_directory_in_bucket(self, bucket_name, bucket_folder, dir_location, is_recursive=True, ignore_list=None):
        dir_list = [f for f in listdir(
            dir_location)]

        if ignore_list is not None:
            dir_list = [f for f in dir_list if f not in ignore_list]

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
                    is_recursive,
                    ignore_list)


    def create_bucket_folder(self, bucket_name, folder_name):
        try:
            response = self.s3_client.Bucket(bucket_name).put_object(ACL='public-read', Body='', Key=folder_name + '/')
        except ClientError:
            print('Was unable to create the folder')
        return response

    def deploy(self, dir_location, environment):
        bucket = environment.get('s3_bucket')
        index_file = environment.get('endpoints').get('index')
        error_file = environment.get('endpoints').get('error')
        ignore_list = environment.get('ignore')

        # response = self.delete_objects_in_bucket(bucket_name)
        try:
            self.s3_client.meta.client.head_bucket(Bucket=bucket)
        except ClientError:
            print("Creating the bucket {0}...".format(bucket))

            region = boto3.session.Session().region_name
            self.s3_client.create_bucket(ACL='public-read',
                                         Bucket=bucket,
                                         CreateBucketConfiguration={'LocationConstraint': region})


        self.put_directory_in_bucket(bucket, None, dir_location, True, ignore_list)

        self.make_bucket_website(bucket, index_file, error_file)

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

    def check_if_bucket_exists(self, bucket_name):
        try:
            boto3.client('s3').head_bucket(Bucket=bucket_name)
        except ClientError as e:
            print(e)
            return False

        return True

    def upload_file_to_s3_bucket(self, bucket_name, file_path, key):
        if not self.check_if_bucket_exists(bucket_name):
            print('Creating the {0} bucket...'.format(bucket_name)) 
        
        bucket = self.s3_client.Bucket(bucket_name)
        filename, file_extension = splitext(file_path)

        print('Uploading file %s...' % key)

        bucket.upload_file(file_path, key, ExtraArgs={
            'ACL': 'public-read', 'ContentType': self.get_file_content_type(file_extension[1:])})



    def undeploy(self, environment):
        bucket = environment.get('s3_bucket')
        response = self.delete_objects_in_bucket(bucket)

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
        
        response = bucket_website.put(
            WebsiteConfiguration={
                'ErrorDocument': {
                    'Key': error_file
                },
                'IndexDocument': {
                    'Suffix': index_file
                }
            }
        )

        region = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        url = '{0}.s3-website-{1}.amazonaws.com'.format(bucket_name, region)
        print('The website address is {0}'.format(url))
