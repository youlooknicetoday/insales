import requests

from insalesapi.config import load_config
from insalesapi.endpoints import (Product, Image, Collection, Order)


class InSalesAPI:

    def __init__(self, hostname, apikey, password):
        self.hostname = f'http://{hostname}'
        self.session = requests.Session()
        self.session.auth = (apikey, password)
        self.session.headers.update({
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'python/insalesapi',
        })
        self.images = Image(self)
        self.products = Product(self)
        self.orders = Order(self)
        self.collections = Collection(self)

    @classmethod
    def from_config(cls, path):
        config = load_config(path)
        return cls(*config)

    def __del__(self):
        self.session.close()
