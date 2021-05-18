import logging

from datetime import datetime
from typing import Optional, Union

from .schemas import Collections, Collection
from ..src.endpoints import BaseController, IterableMixin
from ..src.exceptions import WrongPageNumber


logger = logging.getLogger(__name__)


class CollectionsController(BaseController, IterableMixin):

    def __init__(self):
        self.where = self._filters.get(self.__class__)

    def get_all(
            self, /,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None
    ) -> Collections:
        uri = 'admin/collections.json'
        if per_page and not 10 <= per_page <= 250:
            logger.info('%s', 'Per page param have to be greater or equal 10 and less or equal 250')
        products_list = self._get_all(
            uri, page=page, per_page=per_page, updated_since=updated_since, from_id=from_id).json()
        return Collections(list=products_list)

    def get(self, /, collection_id: Union[int, str]) -> Collection:
        uri = f'admin/collections/{collection_id}.json'
        collection = self._get(uri).json()
        return Collection(**collection)

    def __iter__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass
