from fastapi.encoders import jsonable_encoder
from pydantic import HttpUrl
from typing import Optional, Union

from insalesapi.schemas.images import Images, Image
from .base import BaseController


class ImagesController(BaseController):

    def get_all(self, /, product_id: Union[int, str]) -> list[Image]:
        uri = f'admin/products/{product_id}/images.json'
        images_list = self._get_all(uri).json()
        return Images(list=images_list).list

    def get(self, /, product_id: Union[int, str], image_id: Union[int, str]) -> Image:
        uri = f'admin/products/{product_id}/images/{image_id}.json'
        image = self._get(uri).json()
        return Image(**image)

    def create(
            self, /,
            product_id: Union[int, str],
            filename: str,
            title: Optional[str] = None,
            position: Optional[Union[int, str]] = None,
            image_attachment: Optional[bytes] = None,
            image_url: Optional[HttpUrl] = None
    ) -> Image:
        uri = f'admin/products/{product_id}/images.json'
        if image_url and image_attachment:
            raise ValueError('Only attachment or source url have to be passed')
        elif not image_url and not image_attachment:
            raise ValueError('Neither attachment nor source url was not passed')
        image_json = jsonable_encoder({
            'image': {
                'attachment': image_attachment,
                'src': image_url,
                'filename': filename,
                'title': title,
                'position': position
            }}, exclude_none=True)
        image = self._create(uri, image_json).json()
        return Image(**image)

    def delete(self, /, product_id: Union[int, str], image_id: Union[int, str]) -> bool:
        uri = f'admin/products/{product_id}/images/{image_id}.json'
        response = self._delete(uri)
        return 'ok' in response.json().values()

    def update(
            self, /,
            product_id: Union[int, str],
            image_id: Union[int, str],
            position: Optional[str] = None,
            title: Optional[int] = None
    ) -> Image:
        if not position and not title:
            raise ValueError('At least one value have to be passed')
        uri = f'admin/products/{product_id}/images/{image_id}.json'
        image_json = jsonable_encoder({
            'image': {
                'title': title,
                'position': position
            }}, exclude_none=True)
        image = self._update(uri, image_json).json()
        return Image(**image)

    def __iter__(self):
        images = self.get_all(self.product_id)
        for image in images:
            yield image

    def __call__(self, /, product_id: Union[int, str]):
        self.product_id = product_id
        return self
