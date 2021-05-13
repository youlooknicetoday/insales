import time
import inspect
import logging

from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def request(function):
    def wrapper(obj, uri, *args, **kwargs):
        start = time.time()
        response = function(obj, uri, *args, **kwargs)
        if retry_after := response.headers.get('Retry-After'):
            time.sleep(int(retry_after))
            response = function(obj, uri, *args, **kwargs)
        elif response.status_code not in (200, 201):
            logger.error(
                'status code: %s from %s in %s with %s',
                response.status_code, inspect.stack()[1].function, obj.__class__.__name__, uri)
            raise HTTPError('status code: %s from %s' % (response.status_code, function.__qualname__))
        execution_time = int((time.time() - start) * 1000)
        logger.info(
            'status code: %s, execution time: %s ms, usage limit: %s',
            response.status_code, execution_time, response.headers['API-Usage-Limit'])
        return response
    return wrapper
