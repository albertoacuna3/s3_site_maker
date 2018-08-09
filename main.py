
from os import getcwd
from aws_controller import AWSController
from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults
from cement.core.controller import CementBaseController, expose
from os.path import join
import json

class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'Basic Commands for aws_site_maker'
        arguments = [
            (['-l', '--location'], dict(action='store',
                                        help='specify the directory to run on', metavar='STR')),
            (['-c', '--config'], dict(action='store', help='config file name', metavar='STR')),
            (['-b', '--bucket'], dict(action='store', help='give the bucket name'))
        ]

    def load_config_file(self, config_file_path):
        with open(config_file_path) as f:
            return json.load(f)

    @expose(help="deploy to s3")
    def deploy(self):
        if self.app.pargs.location:
            location = self.app.pargs.location
        else:
            location = getcwd()

        if self.app.pargs.config:
            config_file_path =  join(location, config)
        else:
            config_file_path = join(location, 'aws_site_maker.json')

        config_file = self.load_config_file(config_file_path)

        aws = AWSController()
        aws.put_directory_in_bucket(location, config_file['BucketName'])

    @expose(help='create an s3 bucket', hide=True)
    def create_bucket(self):
        if self.app.pargs.bucket:
            bucket_name = self.app.pargs.bucket
        else:
            print('No bucket name was specified')
            return
        
        aws = AWSController()
        aws.create_s3_bucket(bucket_name, 'private', {'LocationConstraint': 'us-west-2'})

class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        base_controller = 'base'
        handlers = [MyBaseController]


with MyApp() as app:
    app.run()
