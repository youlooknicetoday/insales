import base64
import uuid
from typing import Union, Optional

import requests
from lxml import etree

from .decorators import cool_down
from .exceptions import DataNotProvided
from .src import API


class Endpoint:
    headers = {"Content-Type": "application/xml; charset=utf-8"}
    access = None

    def __new__(cls, *args, **kwargs):
        api = kwargs.pop('api', None)
        if not api and not cls.access:
            raise NotImplementedError
        elif not cls.access and isinstance(api, API):
            cls.access = api
        instance = object.__new__(cls)
        return instance


class Products(Endpoint):

    def get_one(self, product_id: Union[str, int]):
        url = f'{self.access}/admin/products/{product_id}.xml'
        response = requests.get(url)
        data = etree.fromstring(response.content)
        return data.xpath('//title')[0].text


class Images(Endpoint):

    @cool_down
    def get_all(self, product_id: Union[str, int]):
        url = f'{self.access}/admin/products/{product_id}/images.xml'
        response = requests.get(url)
        return response

    @cool_down
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
        response = requests.post(url, data=data, headers=self.headers)
        return response
