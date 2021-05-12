import time
import inspect

from requests.exceptions import HTTPError

from . import logger


def request(function):
    def wrapper(obj, *args, **kwargs):
        start = time.time()
        response = function(obj, *args, **kwargs)
        if retry_after := response.headers.get('Retry-After'):
            time.sleep(int(retry_after))
            response = function(obj, *args, **kwargs)
        elif response.status_code not in (200, 201):
            names = inspect.getfullargspec(function)[0]
            names.remove('self')
            values = dict(zip(names, args))
            logger.error(
                'status code: %s from function %s with %s',
                response.status_code, function.__qualname__, values)
            raise HTTPError('status code: %s from function %s' % (response.status_code, function.__qualname__))
        execution_time = int((time.time() - start) * 1000)
        logger.info(
            'status code: %s, execution time: %s ms, usage limit: %s, function: %s',
            response.status_code, execution_time, response.headers['API-Usage-Limit'], function.__qualname__)
        return response
    return wrapper
