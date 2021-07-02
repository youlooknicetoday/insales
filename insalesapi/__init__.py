from .main import InSalesAPI
from .config import load_config

__all__ = [
    'InSalesAPI'
]


def from_config(config):
    config = load_config(config)
    return InSalesAPI(*config)


def __getattr__(name):
    return name
