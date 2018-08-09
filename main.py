from os import getcwd
from aws_controller import AWSController
from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults
from cement.core.controller import CementBaseController, expose


class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'Basic Commands for aws_site_maker'
        arguments = [
            (['-l', '--location'], dict(action='store',
                                        help='specify the directory to run on', metavar='STR'))
        ]

    @expose(help="deploy to s3")
    def deploy(self):
        if self.app.pargs.location:
            location = self.app.pargs.location
        else:
            location = getcwd()

        aws = AWSController(location)
        aws.put_directory_in_bucket(location)


class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        base_controller = 'base'
        handlers = [MyBaseController]


with MyApp() as app:
    app.run()
