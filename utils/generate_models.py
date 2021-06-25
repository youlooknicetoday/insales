import requests
import subprocess
import tempfile

from functools import cached_property
from lxml import html
from pathlib import Path


class Models:

    """
    This module autogenerate models from official InSales API documentation
    """

    def __init__(self):
        self.url = 'https://api.insales.ru/?doc_format=JSON'
        self.executable = __import__('sys').executable
        self.json = tempfile.NamedTemporaryFile(suffix='.json')
        self.models_path = Path.joinpath(Path(__file__).parent.resolve(), 'models')

    @cached_property
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
        for name, content in self:
            output_filename = Path.joinpath(self.models_path, '%s.py' % name)
            self.json.write(content.encode('utf-8'))
            self.json.seek(0)
            subprocess.run([
                self.executable, '-m', 'json_to_models',
                '-m', name, self.json.name, '-f', 'pydantic', '--datetime', '-o', str(output_filename)],
                check=True, timeout=5, stdout=subprocess.PIPE, universal_newlines=True)
            self.json.truncate()
        self.json.close()

    def __iter__(self):
        for name, route in self.all_routes.items():
            yield name, route


if __name__ == '__main__':
    models = Models()
    models.generate()
