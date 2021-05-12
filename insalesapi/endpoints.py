import uuid
from typing import Union, Optional

import requests
from lxml import etree

from insalesapi.src.decorators import request
from insalesapi.src.exceptions import DataNotProvided
from .src import Endpoint


class Products(Endpoint):

    def get_one(self, product_id: Union[str, int]):
        url = f'{self.access}/admin/products/{product_id}.xml'
        response = requests.get(url)
        data = etree.fromstring(response.content)
        return data.xpath('//title')[0].text


class Images(Endpoint):

    @request
    def get_all(self, product_id: Union[str, int]):
        url = f'{self.access}/admin/products/{product_id}/images.json'
        response = requests.get(url)
        return response

    @request
    def create(
            self,
            product_id: Union[str, int],
            filename: Optional[str] = None,
            image_url: Optional[str] = None,
            image_attachment: Optional[str] = None
    ):
        if not image_url and not image_attachment:
            raise DataNotProvided
        url = f'{self.access}/admin/products/{product_id}/images.xml'
        data = etree.Element('image')
        filename_text = filename or f'{uuid.uuid4()}.png'
        filename = etree.SubElement(data, 'filename')
        filename.text = filename_text
        if image_url:
            image = etree.SubElement(data, 'src')
            image.text = image_url
        elif image_attachment:
            image = etree.SubElement(data, 'attachment')
            image.text = image_attachment
        data = etree.tostring(data, encoding='utf-8', xml_declaration=True, pretty_print=True)
        response = requests.post(url, data=data, headers=self.access.headers)
        return response
