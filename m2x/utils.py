from functools import wraps


def memoize(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        name = '_{0}'.format(func.func_name)
        if not hasattr(self, name):
            result = func(self, *args, **kwargs)
            setattr(self, name, result)
            return result
        return getattr(self, name)
    return wrapper
