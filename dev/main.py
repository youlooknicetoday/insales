import jinja2

import subprocess
import tempfile

from functools import partial
from threading import Lock, Thread
from pathlib import Path

from dev.tools import HtmlDocument, Parser


class Templates:
    """
    Contains template for methods
    Available methods: GET, GET_ALL, COUNT, POST, PUT, DELETE
    """


class Worker:
    """
    Generate directory with endpoints.py and schemas.py
    """

    def __init__(self):
        self.location = Path(__file__).parent.resolve()  # .joinpath('generated')
        self.parser = Parser()
        self.executable = __import__('sys').executable
        self.template = """class {{ resource -}} Controller(BaseController {%- if iterable %}, IterableMixin {%- endif %}):
        {% for function in functions %}

            def {{ function.name }}(self, /, {{ function.params | join(', ') }}) -> {{ resource }}:
            uri = f'{{ function.uri }}'
            data = self._get(uri).json()
            return {{ resource }}(**data)

        {% endfor %}
        """

    def build_endpoint(self):
        pass

    def build_schema(self, file, data):
        """
        :param data: Source
        :param file:
        :return:
        """
        name = data['resource'].lower()
        data = data['json']
        location = self.location.joinpath('generated', name)
        location.mkdir(parents=True)
        output_filename = location.joinpath('schemas.py')
        file.write(data.encode('utf-8'))
        file.seek(0)
        subprocess.run([
            self.executable, '-m', 'json_to_models',
            '-m', name, file.name, '-f', 'pydantic', '--datetime', '-o', str(output_filename)],
            check=True, timeout=5, stdout=subprocess.PIPE, universal_newlines=True)
        file.truncate()

    def build(self):
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

    def run(self):
        lock = Lock()
        document = HtmlDocument.from_url()
        self.parser.feed(document)
        ctx = self.parser.generate_context()
        _ctx = [(c, lock) for c in ctx if c.get('json')]
        with tempfile.NamedTemporaryFile(suffix='.json') as file, Pool(max_workers=4) as pool:
            build_schema = partial(self.build_schema, file)
            pool.map(build_schema, _ctx)

