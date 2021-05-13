import configparser
import logging

from typing import Union
from pathlib import Path

from .endpoints import BaseController
from ..where.endpoints import register_builders

logger = logging.getLogger(__name__)


def init_credentials(path: Union[str, Path]) -> bool:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    config = configparser.ConfigParser()
    config.read(path)
    access = 'http://%(apikey)s:%(password)s@%(hostname)s' % config['insales']
    base = BaseController(access=access)
    if base.connection_established:
        register_builders()
        logger.info("%s", "Successfully initialized")
        return True
    logger.error('%s', "Can't initialize")
    return False
