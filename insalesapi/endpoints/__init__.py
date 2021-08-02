from .products import ProductsController
from .images import ImagesController


class EndpointsMixin:

    @property
    def product(self):
        return ProductsController(self.request)

    @property
    def image(self):
        return ImagesController(self.request)


__all__ = ('EndpointsMixin', )
