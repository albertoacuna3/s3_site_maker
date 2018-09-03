import json
import sys
import os

CONFIG_FILE_TEMPLATE = """{
    "dev": {
        "s3_bucket" : "*",
        "ignore" : [],
        "endpoints": {
            "index": "*",
            "error": "*"
        }
    }
}"""

AVAILABLE_REGIONS = {
    'US East (Ohio)' :	'us-east-2',
    'US East (N. Virginia)' : 'us-east-1',
    'US West (N. California)' :	'us-west-1',
    'US West (Oregon)' : 'us-west-2',
    'Canada (Central)': 'ca-central-1',
    'Asia Pacific (Mumbai)': 'ap-south-1',
    'Asia Pacific (Seoul)': 'ap-northeast-2',
    'Asia Pacific (Osaka-Local)': 'ap-northeast-3',
    'Asia Pacific (Singapore)': 'ap-southeast-1',
    'Asia Pacific (Sydney)': 'ap-southeast-2',
    'Asia Pacific (Tokyo)': 'ap-northeast-1',
    'China (Beijing)': 'cn-north-1',
    'China (Ningxia)': 'cn-northwest-1',
    'EU (Frankfurt)': 'eu-central-1',
    'EU (Ireland)': 'eu-west-1',
    'EU (London)': 'eu-west-2',
    'EU (Paris)': 'eu-west-3',
    'South America (Sao Paulo)': 'sa-east-1'
}

class Core:
    config_file_template = CONFIG_FILE_TEMPLATE

    #Creates the aws_site_maker.json file
    def init(self):
        bucket_name = input('Enter the bucket name: ')
        index_file = input('Name of the index html file (default: index.html): ')
        error_file = input('Name of the error html file (default: error.html): ')

        if not index_file:
            index_file = 'index.html'
        if not error_file:
            error_file = 'error.html'

        config_file_template_obj = json.loads(self.config_file_template)
        config_file_template_obj['dev']['s3_bucket'] = bucket_name
        config_file_template_obj['dev']['endpoints']['index'] = index_file
        config_file_template_obj['dev']['endpoints']['error'] = error_file

        with open('aws_site_maker.json', 'w') as f:
            json.dump(config_file_template_obj, f)


    def load_config_file(self, config_file_path='aws_site_maker.json'):
        if os.path.exists(config_file_path):
            with open(config_file_path) as f:
                try:
                    self.config_file = json.load(f)
                except:
                    print('Was not able to load the json file')
        else:
            print('The config file at {0} does not exist or was not able to be read.'.format(config_file_path))


    ###############CONFIG FILE METHODS#####################
    def get_environment(self, environment_name):
        try:
            return self.config_file['Environments'][environment_name]
        except KeyError:
            print('The environment {0} was not found in the config file...'.format(environment_name))
            sys.exit(1)
        # response = self.delete_objects_in_bucket(bucket_name)

    def get_bucket_name(self):
        BUCKET_CONST = 's3_bucket'

        try:
            return self.environment[BUCKET_CONST]
        except:
            print('Could not find a bucket name in the config file...')
            sys.exit(1)
