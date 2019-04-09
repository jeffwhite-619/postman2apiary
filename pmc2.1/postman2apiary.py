"""
    Tool for generating Blueprint API markup or the Apiary API
    from a Postman collection
    Author: Paul Kinuthia
"""

import json
import traceback
import sys
from urllib.parse import urlparse


class PostmanToApiary:
    def __init__(self, data: dict = {}):
        self.file = data.get('postman_collection')
        self.data = {}
        self.name = ''
        self.description = ''
        self.domain = ''
        self.api_version = data.get('api_version')
        self.output_file = data.get('output_file')
        self.file_format = 'FORMAT: 1A'
        self.requests = []
        self.verbose = data.get('verbose')
        self.pm_version = data.get('postman_collection_version')
        self.requests = []
        self.get_data()

    def get_data(self):
        try:
            with open(self.file, encoding='utf-8') as f:
                self.data = json.loads(f.read())
        except Exception as e:
            self.handle_exception(e)
        self.name = self.data.get('name', '')
        self.description = self.data.get('description', '')
        self.get_url_info()

    def write(self):
        # write document introduction
        doc = open(self.output_file, 'w+')
        doc.write(self.file_format + '\n')
        doc.write('HOST: ' + self.domain + '\n\n')
        doc.write('# ' + self.name + '\n\n')
        if self.description:
            doc.write(self.description)
        doc.close()
        self.process_collection()

    def process_collection(self):
        for request in self.requests:
            self.process_requests(request)

    def get_requests(self):
        if self.pm_version == 'v2':
            self.requests = self.data.get('requests')
        elif self.pm_version == 'v2.1':
            info = self.data.get('info')
            items = self.data.get('item')
            if not info or not items:
                print('Postman collection is not v2.1')
                exit(0)
            for item in items:
                self.requests.append(item.get('request'))
        else:
            print('No requests found, aborting...')
            exit(0)

    def process_requests(self, request):
        url = urlparse(request.get('url'))
        path = url.path.replace(self.api_version, '')
        self.domain, description = url, request.get('description')
        method, name = request.get('method', ''), request.get('name', '')
        content_type = 'application/json'
        collection_name = '## ' + name + ' [' + path + ']\n'
        title = '### ' + name + ' [' + method + ']'
        req = '+ Request (' + content_type + ')'
        resp = '+ Response 201 (' + content_type + ')'

        doc = open(self.output_file, 'a')
        doc.write(collection_name + '\n\n')
        doc.write(title + '\n')
        doc.write(description + '\n\n')
        try:
            if method == "POST":
                doc.write(req + '\n\n')
                json_data = json.loads(request.get('rawModeData'))
                json.dump(json_data, doc, indent=8, sort_keys=True, ensure_ascii=False)
                doc.write('\n\n\n')
        except Exception as e:
            self.handle_exception(e, False)

        doc.write(resp + '\n\n\n')
        doc.close()

    def get_url_info(self):
        try:
            self.get_requests()
            url = self.requests[0].get('url')
            if self.pm_version == 'v2.1':
                url = url.get('raw')
            domain = urlparse(url)
            self.domain = url.replace(domain.path, '')
            if len(self.api_version) > 0:
                self.domain = self.domain + self.api_version
        except Exception as e:
            self.handle_exception(e)

    def handle_exception(self, e: Exception, fault: bool = True):
        print('[x] :( Some error occurred')
        print(e)
        if self.verbose:
            traceback.print_exc(file=sys.stdout)
        if fault:
            exit(0)
        else:
            pass
