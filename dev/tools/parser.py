import re

from lxml import html
from .document import HtmlDocument


class Parser:
    """
    This class is responsible for parsing the documentation page source code.
    It finds resource sections, then all the methods for each resource.
    """

    def __init__(self):
        self.pattern_of_get_uri = re.compile(r'\d\.json$')
        self.pattern_of_param_names = re.compile(r'\[([^\]]+)?\]')
        self.data = None

    def feed(self, document: HtmlDocument):
        self.data = document

    def parse_method_param(self, param: str, /, required: bool):
        if match := self.pattern_of_param_names.findall(param):
            param = match[-1]
        if not required:
            param = '%s=None' % param
        return param

    def parse_table(self, table: html.HtmlElement) -> list[str, ...]:
        params = list()
        table_width = len(table.xpath('./tr/th'))
        for cell in table.xpath('./tr/td')[::table_width]:
            required = True if cell.xpath('./span[contains(@class, "required")]') else False
            param = self.parse_method_param(cell.text, required=required)
            params.append(param)
        return params

    def parse_method(self, node: html.HtmlElement) -> tuple[dict, bool]:
        with_json = False
        http_method, uri = node.xpath('.//section[@class="route"]/pre')[0].text.split()
        data = {'http_method': http_method, 'uri': uri}
        params_table = node.xpath('./section[@class="params"]/div/table')
        if params_table:
            params = self.parse_table(params_table[0])
            data['params'] = params
        if http_method == 'GET' and self.pattern_of_get_uri.search(uri):
            data['model'] = node.xpath('.//section[@class="body"]/pre/code')[0].text_content()
            with_json = True
        return data, with_json

    def generate_context(self):
        result = list()
        for resource in self.data.resources:
            context = {'resource': resource.name, 'functions': []}
            for method in resource.methods:
                data, with_json = self.parse_method(method.node)
                data['name'] = method.name
                if with_json:
                    context['json'] = data.pop('model')
                context['functions'].append(data)
            result.append(context)
        return result
