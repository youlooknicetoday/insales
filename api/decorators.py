import time


def cool_down(function):
    def wrapper(*args, **kwargs):
        content, headers = function(*args, **kwargs)
        if retry_after := headers.get('Retry-After'):
            time.sleep(int(retry_after))
            content, headers = function(*args, **kwargs)
        return content, headers
    return wrapper
