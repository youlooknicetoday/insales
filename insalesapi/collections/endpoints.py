from datetime import datetime
from typing import Optional, Union

from ..src import logger
from ..src.endpoints import BaseController, IterableMixin
from ..src.exceptions import WrongPageNumber


class CollectionsController(BaseController, IterableMixin):

    def get_all(
            self, /,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None
    ) -> 'Collections':
        uri = 'admin/collections.json'
        if per_page and not 10 <= per_page <= 250:
            logger.info('%s', 'Per page param have to be greater or equal 10 and less or equal 250')
        products_list = self._get_all(
            uri, page=page, per_page=per_page, updated_since=updated_since, from_id=from_id).json()
        return Products(list=products_list)

    def get(self, /, collection_id: Union[int, str]) -> 'Collection':
        uri = f'admin/collections/{collection_id}.json'
        product = self._get(uri).json()
        return product

    def __iter__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass
