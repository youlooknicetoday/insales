import configparser
import logging

from base64 import b64encode
from typing import Union
from pathlib import Path

from .endpoints import BaseController
from .filters import register_filters

logger = logging.getLogger(__name__)


def init_credentials(path: Union[str, Path]) -> bool:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    config = configparser.ConfigParser()
    config.read(path)
    auth, hostname = (
        '%(apikey)s:%(password)s' % config['insales'],
        'http://%(hostname)s' % config['insales']
    )
    auth = b64encode(auth.encode('utf-8')).decode('utf-8')
    BaseController.headers['Authorization'] = f'Basic {auth}'
    BaseController.hostname = hostname
    base = BaseController()
    if base.connection_established:
        base_filters = register_filters()
        base.register_filters(base_filters)
        logger.info("%s", "Successfully initialized")
        return True
    logger.error('%s', "Can't initialize")
    return False
