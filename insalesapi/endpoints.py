from .images.endpoints import ImagesController as Image
from .products.endpoints import ProductsController as Product
from .collections.endpoints import CollectionsController as Collection

__all__ = [
    'Image',
    'Product',
    'Collection',
]
