import time


def cool_down(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if retry_after := response.headers.get('Retry-After'):
            time.sleep(int(retry_after))
            response = function(*args, **kwargs)
        return response
    return wrapper
