import re
import requests
import subprocess
import tempfile

from lxml import html
from lxml.html import HtmlElement
from pathlib import Path


class templates:

    DISPATCHER = {
        lambda request: request.removesuffix('-json').endswith('s'): 'get_all',
        lambda request: 'count' in request: 'count',
        lambda request: 'get' in request: 'get',
        lambda request: any(item in request for item in ('add', 'create', 'decline')): 'create',
        lambda request: any(item in request for item in ('move', 'update')): 'update',
        lambda request: any(item in request for item in ('delete', 'destroy', 'remove')): 'delete'
    }

    def __init__(self, classname, actions: list[tuple[str, HtmlElement]]):
        self.classname = classname
        self.actions = actions
        self.result = []

    def process(self):
        for action, node in self.actions:
            self.generate(action, node)

    def generate(self, action: str, node):
        # preprocess node
        return {
            'get': self.generate_get
        }[action](1, 2, 3)

    def generate_get(self, function_params, uri, return_type):
        uri = re.sub(r'\d', function_params, uri)
        return """
        def get({function_params}) -> {return_type}:
            uri = f'{uri}'
            data = self._get(uri).json()
            return {return_type}(**data)
        """.format(function_params=function_params, uri=uri, return_type=return_type)

    @classmethod
    def generate_update(cls):
        ...


class Models:

    """
    This module autogenerate models from official InSales API documentation
    """
    NS = {"re": "http://exslt.org/regular-expressions"}

    def __init__(self):
        self.url = 'https://api.insales.ru/?doc_format=JSON'
        self.page_source_code = None
        self.executable = __import__('sys').executable
        self.location = Path(__file__).parent.resolve().joinpath('generated')

    def check_dir(self):
        if not self.location.exists():
            self.location.mkdir()

    def load_file(self, filename='InSales_API.html'):
        if self.page_source_code is None:
            file = self.location.parent.joinpath(filename)
            if file.is_file():
                self.page_source_code = html.parse(str(file))
            else:
                response = requests.get(self.url)
                self.page_source_code: HtmlElement = html.fromstring(response.content)
                self.page_source_code.getroottree().write(str(file))
        return self.page_source_code

    def dispatch_request(self, request):
        return {
            request.removesuffix('-json').endswith('s'): 'get_all',
            'count' in request: 'count', 'get' in request: 'get',
            any(item in request for item in ('add', 'create', 'decline')): 'create',
            any(item in request for item in ('move', 'update')): 'update',
            any(item in request for item in ('delete', 'destroy', 'remove')): 'delete'
        }.get(True, request)

    def generate_endpoints(self):
        for resource in self.page_source_code.xpath('//h2'):
            name = resource.text.replace(' ', '')

            for article in resource.itersiblings():
                result = self.dispatch_request(article.attrib['id'])
                if result == 'get' and article.attrib['id'].removesuffix('-json').endswith('s'):
                    result = 'get_all'
                elif 'count' in article.attrib['id']:
                    result = 'count'

    @property
    def all_routes(self):
        response = requests.get(self.url)
        page_source_code = html.fromstring(response.content)
        nodes = page_source_code.xpath('//pre[starts-with(text (), "GET") and not(contains(text (), "s.json"))]')
        return {
            node.xpath('./ancestor::section/h2')[0].text:
                node.xpath('./ancestor::div[@class="request"]/following-sibling::div/section[@class="body"]/pre/code')[0].text_content()
            for node in nodes
        }

    def generate(self):
        self.check_dir()
        with tempfile.NamedTemporaryFile(suffix='.json') as file:
            for name, content in self.all_routes.items():
                output_filename = Path.joinpath(self.location, '%s.py' % name)
                file.write(content.encode('utf-8'))
                file.seek(0)
                subprocess.run([
                    self.executable, '-m', 'json_to_models',
                    '-m', name, file.name, '-f', 'pydantic', '--datetime', '-o', str(output_filename)],
                    check=True, timeout=5, stdout=subprocess.PIPE, universal_newlines=True)
                file.truncate()


if __name__ == '__main__':
    models = Models()
    models.generate()
