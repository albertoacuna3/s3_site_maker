from os import getcwd
from aws_controller import AWSController
from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults
from cement.core.controller import CementBaseController, expose
from os.path import join
import json
from core import Core

class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'Basic Commands for aws_site_maker'
        arguments = [
            (['-l', '--location'], dict(action='store',
                                        help='specify the directory to run on', metavar='STR')),
            (['-c', '--config'], dict(action='store',
                                      help='config file name', metavar='STR')),
            (['extra_arguments'], dict(action='store', nargs='*'))
        ]

    def load_config_file(self, config_file_path):
        with open(config_file_path) as f:
            return json.load(f)

    def get_config_file_path(self):
        if self.app.pargs.location:
            location = self.app.pargs.location
        else:
            location = getcwd()

        if self.app.pargs.config:
            config_file_path = join(location, self.app.pargs.config)
        else:
            config_file_path = join(location, 'aws_site_maker.json')

        return config_file_path

    @expose(help='Initiate the aws_site_maker settings')
    def init(self):
        core = Core()
        core.init()        

    @expose(help="deploy to s3")
    def deploy(self):
        if self.app.pargs.extra_arguments[0]:
            environment = self.app.pargs.extra_arguments[0]
        else:
            print('Please specify an environment')
            return

        config_file = self.load_config_file(self.get_config_file_path())

        if self.app.pargs.location:
            location = self.app.pargs.location
        else:
            location = getcwd()

        aws = AWSController()
        aws.deploy(location, config_file['Environments'][environment])

    @expose(help='create an s3 bucket', hide=False)
    def create_bucket(self):
        if self.app.pargs.extra_arguments[0]:
            bucket_name = self.app.pargs.extra_arguments[0]
        else:
            print('No bucket name was specified')
            return

        aws = AWSController()
        aws.create_s3_bucket(bucket_name, 'private', {
                             'LocationConstraint': 'us-west-2'})

    @expose(help='undeploy the environment')
    def undeploy(self):
        if self.app.pargs.extra_arguments[0]:
            environment = self.app.pargs.extra_arguments[0]
        else:
            print('Please specify an environment')
            return

        config_file = self.load_config_file(self.get_config_file_path())
        environment = config_file['Environments'][environment]
        aws = AWSController()
        aws.undeploy(environment)


class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        base_controller = 'base'
        handlers = [MyBaseController]


with MyApp() as app:
    app.run()
