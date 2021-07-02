import jinja2
import re
import requests
import subprocess
import tempfile

from lxml import html
from pathlib import Path


class Parser:
    """
    This class is responsible for parsing the documentation page source code.
    It finds resource sections, then all the methods for each resource.
    """

    def __init__(self, location):
        self.location = location
        self.url = 'https://api.insales.ru/?doc_format=JSON'
        self.pattern = re.compile(r'\d\.json$')
        self.html_source_code = None

    def load_file(self, filename='InSalesAPI.html', save_file=False) -> html.HtmlElement:
        if self.html_source_code:
            return self.html_source_code

        filepath = self.location.parent.joinpath(filename)
        if filepath.is_file():
            self.html_source_code = html.parse(str(filepath))
        else:
            response = requests.get(self.url)
            self.html_source_code = html.fromstring(response.content)
            if save_file:
                self.html_source_code.getroottree().write(str(filepath))
        return self.html_source_code

    @property
    def resources(self) -> dict[str, html.HtmlElement]:
        return {
            node.xpath('./h2')[0].text.replace(' ', ''): node
            for node in self.html_source_code.xpath('//section[@class="example"]')
        }

    @property
    def methods(self):
        result = dict()
        for name, resource in self.resources.items():
            methods = resource.xpath('./article')
            keys = map(lambda elem: elem.xpath('./h3/text()')[0].strip().replace(' ', '_').lower(), methods)
            result[name] = dict(zip(keys, methods))
        return result

    def parse_table(self, table) -> list[str, ...]:
        result = list()
        for cell in table.xpath('./tr/td')[::2]:
            name = cell.text
            if not cell.xpath('./span[@class="required"]'):
                name = '%s=None' % name
            result.append(name)
        return result

    def parse_method(self, node) -> tuple[dict, bool]:
        with_json = False
        http_method, uri = node.xpath('.//section[@class="route"]/pre')[0].text.split()
        data = {'http_method': http_method, 'uri': uri}
        params_table = node.xpath('./section[@class="params"]/div/table')
        if params_table:
            params = self.parse_table(params_table[0])
            data['params'] = params
        if http_method == 'GET' and self.pattern.search(uri):
            data['model'] = node.xpath('.//section[@class="body"]/pre/code')[0].text_content()
            with_json = True
        return data, with_json

    def generate_context(self):
        result = list()
        for resource, methods in self.methods.items():
            context = {'resource': resource, 'functions': []}
            for method_name, node in methods.items():
                data, with_json = self.parse_method(node)
                data['name'] = method_name
                if with_json:
                    context['json'] = data.pop('model')
                context['functions'].append(data)
            result.append(context)
        return result


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
        self.tpl = """class {{ resource -}} Controller(BaseController {%- if iterable %}, IterableMixin {%- endif %}):
        {% for function in functions %}

            def {{ function.name }}(self, /, {{ function.params | join(', ') }}) -> {{ resource }}:
            uri = f'{{ function.uri }}'
            data = self._get(uri).json()
            return {{ resource }}(**data)

        {% endfor %}
        """

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
        self.location = Path(__file__).parent.resolve()  # .joinpath('generated')
        self.parser = Parser(self.location)
        self.templates = Templates()
        self.executable = __import__('sys').executable

    def build_endpoint(self):
        pass

    def build_schema(self, data, name, path, file):
        """
        :param data: Source
        :param name:
        :param path:
        :param file:
        :return:
        """
        output_filename = path.joinpath('schemas.py')
        file.write(data.encode('utf-8'))
        file.seek(0)
        subprocess.run([
            self.executable, '-m', 'json_to_models',
            '-m', name, file.name, '-f', 'pydantic', '--datetime', '-o', str(output_filename)],
            check=True, timeout=5, stdout=subprocess.PIPE, universal_newlines=True)
        file.truncate()

    def build(self):
        if self.parser.html_source_code is None:
            self.parser.load_file()
        with tempfile.NamedTemporaryFile(suffix='.json') as file:
            for name, resource in self.parser.resources.items():
                location = self.location.joinpath(name.lower())
                location.mkdir()
                self.build_schema('data', name, location, file)  # have to return data from GET method
                methods = self.parser.find_methods(resource)
                endpoint = []
                for method in methods:
                    template = self.templates.generate(method)
                    endpoint.append(template)
