def exclude_none(params):
    return {key: value for key, value in params.items() if value is not None}


BaseController = type('BaseController', (), {'__init__': lambda self, request: setattr(self, '_request', request)})
