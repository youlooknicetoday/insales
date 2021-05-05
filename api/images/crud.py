from lxml import etree
from pathlib import Path
from typing import Union, Optional

import base64
import requests
import uuid

from ..crud import Base
from ..decorators import cool_down


class CRUD(Base):

    @cool_down
    def get_all_pictures(self, product_id: Union[str, int]):
        url = f'{self.api}/admin/products/{product_id}/images.xml'
        response = requests.get(url)
        return response.content, response.headers

    @cool_down
    def create_image(
            self,
            product_id: Union[str, int],
            filename: Optional[str] = None,
            image_url: Optional[str] = None,
            image_attachment: Optional[str] = None
    ):
        if not image_url and not image_attachment:
            raise
        url = f'{self.api}/admin/products/{product_id}/images.xml'
        data = etree.Element('image')
        filename_text = filename or f'{uuid.uuid4()}.jpg'
        filename = etree.SubElement(data, 'filename')
        filename.text = filename_text
        if image_url:
            image = etree.SubElement(data, 'src')
            image.text = image_url
        elif image_attachment:
            image = etree.SubElement(data, 'attachment')
            image_text = base64.b64encode(image_attachment).decode('utf-8')
            image.text = image_text
        data = etree.tostring(data, encoding='utf-8', xml_declaration=True, pretty_print=True)
        response = requests.post(url, data=data, headers=self.api.headers)
        return response.content, response.headers
