import json

class Core:
    def init(self):
        bucket_name = input('Enter the bucket name: ')
        template = {}
        template['Environments'] = {}
        template['Environments']['dev'] = {}
        template['Environments']['dev']['Buckets'] = { 'Main': bucket_name }

        print(json.dumps(template, ensure_ascii=False))

        with open('aws_site_maker.json', 'w') as f:
            f.write(json.dump(template, ensure_ascii=False))

