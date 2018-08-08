import os
import boto3
import json
from os import listdir, getcwd
from os.path import isfile, join

from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults

class AWSController:
    def __init__(self, location):
        self.location = location
        self.s3 = boto3.resource('s3')
        self.config_file = self.load_config_file()
        self.s3_bucket = self.load_s3_bucket_object()

    def load_s3_bucket_object(self):
        if self.config_file is None:
            self.load_config_file()

        self.s3_bucket = self.s3.Bucket(self.config_file['BucketName'])

    def put_directory_in_bucket(self, location):
        if self.s3_bucket is None:
            self.load_s3_bucket_object()

        files_only = [f for f in listdir(location) if isfile(join(location, f))]
        for fn in files_only:
            filename, file_extension = os.path.splitext(fn)
            self.s3_bucket.upload_file(join(location, fn), fn, ExtraArgs={'ACL':'public-read', 'ContentType': self.get_file_content_type(file_extension[1:])})

    def get_file_content_type(self, filename_ext):
        mimetypes = {
        'html': 'text/html',
        'json': 'application/json',
        'css': 'text/css',
        'other': 'text/plain'
        }

        return mimetypes.get(filename_ext, mimetypes.get('other'))

    def get_bucket_objects(self, bucket):
        response =  self.s3.meta.client.list_objects(
            Bucket=bucket
        )
        contents = response['Contents']
        formatted_contents = [{'Key': d['Key'], 'Size': d['Size'], 'LastModified': d['LastModified'].strftime("%B %d, %Y")} for d in contents]
        return formatted_contents

    def get_current_directory(self):
        return os.getcwd()

    def push_files_to_s3(self, filename, bucket, filename_key):
        #TODO: Load files to S3
        self.s3.meta.client.upload_file(filename, bucket, filename_key)

    def load_config_file(self):
        config_file = join(self.location, 'aws_site_maker.json')
        with open(config_file) as f:
            self.config_file = json.load(f)



# define our default configuration options
defaults = init_defaults('myapp')
defaults['myapp']['debug'] = False
defaults['myapp']['some_param'] = 'some value'

# define any hook functions here
def my_cleanup_hook(app):
    pass

class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        config_defaults = defaults
        hooks = [
            ('pre_close', my_cleanup_hook),
        ]

with MyApp() as app:
    app.args.add_argument('-l', '--location', action='store', metavar='STR', help='the directory you want to run this on')

    app.run()

    if app.pargs.location:
        location = app.pargs.location
        aws = AWSController(location)
        aws.put_directory_in_bucket(location)
