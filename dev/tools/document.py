import requests

from pathlib import Path
from lxml import html


class HtmlNode:

    def __init__(self, node: html.HtmlElement):
        self.node = node


class Method(HtmlNode):

    @property
    def name(self):
        return self.node.xpath('./h3/text()')[0].strip().replace(' ', '_').lower()


class Resource(HtmlNode):

    @property
    def name(self):
        return self.node.xpath('./h2')[0].text.replace(' ', '')

    @property
    def methods(self):
        return [Method(node=node) for node in self.node.xpath('./article')]


class HtmlDocument:

    def __init__(self, *, source_code: html.HtmlElement):
        self.source_code = source_code

    @property
    def resources(self):
        return [Resource(node=node) for node in self.source_code.xpath('//section[@class="example"]')]

    @classmethod
    def from_file(cls, filepath=None):
        source_code = html.parse(str(filepath))
        return cls(source_code=source_code)

    @classmethod
    def from_url(cls, url='https://api.insales.ru/?doc_format=JSON'):
        response = requests.get(url)
        source_code = html.fromstring(response.content)
        return cls(source_code=source_code)
