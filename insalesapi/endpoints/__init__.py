from .products import ProductsController
from .images import ImagesController
from .orders import OrdersController


class EndpointsMixin:
    
    request = None

    @property
    def product(self):
        return ProductsController(self.request)

    @property
    def image(self):
        return ImagesController(self.request)
    
    @property
    def order(self):
        return OrdersController(self.request)


__all__ = ('EndpointsMixin', )
