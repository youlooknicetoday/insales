import subprocess
import tempfile

from lxml import html
from pathlib import Path


class Parser:
    """
    This class is responsible for parsing the documentation source code.
    It finds resource sections, then all the methods for each resource.
    """

    def load_file(self):
        pass

    def _find_resources(self) -> list[html.HtmlElement]:
        pass

    @property
    def resources(self):
        return {node.xpath('./h2')[0].text.replace(' ', ''): node for node in self._find_resources()}

    def find_methods(self, resource):
        # what about uri, params, json?
        # parse GET to GET_ALL or COUNT
        pass


class Templates:
    """
    Contains template for methods
    Available methods: GET, GET_ALL, COUNT, POST, PUT, DELETE
    """
    def __init__(self):
        self.manager = {
            'GET': self.get, 'GET_ALL': self.get_all, 'COUNT': self.count,
            'POST': self.create, 'PUT': self.update, 'DELETE': self.delete,
        }
        self._function_params = ['self', '/']

    def generate(self, method, **kwargs):
        return self.manager[method](**kwargs)

    def get(self, **kwargs):
        pass

    def get_all(self, **kwargs):
        pass

    def count(self, **kwargs):
        pass

    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class Builder:
    """
    Generate directory with endpoints.py and schemas.py
    """

    def __init__(self):
        self.parser = Parser()
        self.templates = Templates()
        self.location = Path(__file__).parent.resolve().joinpath('generated')
        self.file = tempfile.NamedTemporaryFile(suffix='.json')
        self.executable = __import__('sys').executable

    def build_endpoint(self):
        pass

    def build_schema(self, data, name, path):
        output_filename = path.joinpath('schemas.py')
        self.file.write(data.encode('utf-8'))
        self.file.seek(0)
        subprocess.run([
            self.executable, '-m', 'json_to_models',
            '-m', name, self.file.name, '-f', 'pydantic', '--datetime', '-o', str(output_filename)],
            check=True, timeout=5, stdout=subprocess.PIPE, universal_newlines=True)
        self.file.truncate()

    def build(self):
        self.parser.load_file()
        for name, resource in self.parser.resources.items():
            location = self.location.joinpath(name.lower())
            location.mkdir()
            self.build_schema('data', name, location)  # have to return data from GET method
            methods = self.parser.find_methods(resource)
            endpoint = []
            for method in methods:
                template = self.templates.generate(method)
                endpoint.append(template)
        self.file.close()
