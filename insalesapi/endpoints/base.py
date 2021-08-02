def exclude_none(self, params):
    return {
        key: exclude_none(self, value) if isinstance(value, dict)
        else value for key, value in params.items() if value
    }


BaseController = type(
    'BaseController', (), {
        '__init__': lambda self, request: setattr(self, '_request', request),
        'exclude_none': exclude_none,
    }
)
