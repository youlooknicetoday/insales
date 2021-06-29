import re
import requests
import subprocess
import tempfile

from lxml import html
from lxml.html import HtmlElement
from pathlib import Path


class templates:

    DISPATCHER = {
        lambda uri: uri.removesuffix('-json').endswith('s'): 'get_all',
        lambda uri: 'count' in uri: 'count', lambda uri: 'get' in uri: 'get',
        lambda uri: any(item in uri for item in ('add', 'create', 'decline')): 'create',
        lambda uri: any(item in uri for item in ('move', 'update')): 'update',
        lambda uri: any(item in uri for item in ('delete', 'destroy', 'remove')): 'delete'
    }

    def __init__(self, classname, actions: list[HtmlElement]):
        self.classname = classname
        self.actions = actions
        self.result = []

    def process(self):
        for action in self.actions:
            for key, value in self.__class__.DISPATCHER.items():
                if key(action.attrib['id']):
                    result = value
                    break

    def generate_get(self, function_params, uri, return_type):
        uri = re.sub(r'\d', function_params, uri)
        return """
        def get({function_params}) -> {return_type}:
            uri = f'{uri}'
            data = self._get(uri).json()
            return {return_type}(**data)
        """.format(function_params=function_params, uri=uri, return_type=return_type)


class Codegen:

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

    def load_file(self, filename='InSales_API.html', save_file=False):
        if self.page_source_code is None:
            filepath = self.location.parent.joinpath(filename)
            if filepath.is_file():
                self.page_source_code = html.parse(str(filepath))
            else:
                response = requests.get(self.url)
                self.page_source_code = html.fromstring(response.content)
                if save_file:
                    self.page_source_code.getroottree().write(str(filepath))
        return self.page_source_code

    def generate_endpoints(self):
        for resource in self.page_source_code.xpath('//h2'):
            name = resource.text.replace(' ', '')
            articles = [article for article in resource.itersiblings()]
            template = templates(name, articles)
            template.process()

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
    worker = Codegen()
    worker.generate()
