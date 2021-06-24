import requests

from .endpoints import (Product, Image, Collection)


class InSalesAPI:

    def __init__(self, hostname, apikey, password):
        self.hostname = f'http://{hostname}'
        self.session = requests.Session()
        self.session.auth = (apikey, password)

        self.images = Image(self)
        self.products = Product(self)

    def __del__(self):
        self.session.close()
