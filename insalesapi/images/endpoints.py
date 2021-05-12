import requests

from fastapi.encoders import jsonable_encoder
from pydantic import HttpUrl
from typing import Optional, Union

from .schemas import Images, Image
from ..src import Endpoint
from ..src.exceptions import DataNotProvided
from ..src.decorators import request


class ImagesController(Endpoint):

    @request
    def _get_all(self, product_id: Union[int, str]) -> requests.Response:
        url = f'{self.access}/admin/products/{product_id}/images.json'
        response = requests.get(url)
        return response

    def get_all(self, /, product_id: Union[int, str]) -> Images:
        images_list = self._get_all(product_id).json()
        return Images(list=images_list)

    @request
    def _get(self, product_id: Union[int, str], image_id: Union[int, str]) -> requests.Response:
        url = f'{self.access}/admin/products/{product_id}/images/{image_id}.json'
        response = requests.get(url)
        return response

    def get(self, /, product_id: Union[int, str], image_id: Union[int, str]) -> Image:
        image = self._get(product_id, image_id).json()
        return Image(**image)

    @request
    def _create(self, product_id: Union[int, str], image_json: dict) -> requests.Response:
        url = f'{self.access}/admin/products/{product_id}/images.json'
        response = requests.post(url, json=image_json)
        return response

    def create(
            self, /,
            product_id: Union[int, str],
            filename: str,
            title: Optional[str] = None,
            position: Optional[Union[int, str]] = None,
            image_attachment: Optional[bytes] = None,
            image_url: Optional[HttpUrl] = None
    ) -> Image:
        if image_url and image_attachment:
            raise ValueError('Only attachment or src url have to be passed')
        elif not image_url and not image_attachment:
            raise DataNotProvided('Neither attachment nor src url was not passed')
        image_json = jsonable_encoder({
            'image': {
                'attachment': image_attachment,
                'src': image_url,
                'filename': filename,
                'title': title,
                'position': position
            }}, exclude_none=True)
        image = self._create(product_id, image_json).json()
        return Image(**image)

    @request
    def _delete(self, product_id: Union[int, str], image_id: Union[int, str]) -> requests.Response:
        url = f'{self.access}/admin/products/{product_id}/images/{image_id}.json'
        response = requests.delete(url)
        return response

    def delete(self, /, product_id: Union[int, str], image_id: Union[int, str]) -> bool:
        response = self._delete(product_id, image_id)
        return 'ok' in response.json().values()

    @request
    def _update(self, product_id: Union[int, str], image_id: Union[int, str], image_json: dict) -> requests.Response:
        url = f'{self.access}/admin/products/{product_id}/images/{image_id}.json'
        response = requests.put(url, json=image_json)
        return response

    def update(
            self, /,
            product_id: Union[int, str],
            image_id: Union[int, str],
            position: Optional[str] = None,
            title: Optional[int] = None
    ) -> Image:
        if not position and not title:
            raise DataNotProvided('At least one value have to be passed')
        image_json = jsonable_encoder({
            'image': {
                'title': title,
                'position': position
            }}, exclude_none=True)
        image = self._update(product_id, image_id, image_json).json()
        return Image(**image)
