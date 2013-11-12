from functools import wraps
from datetime import date, datetime

from iso8601 import iso8601


def memoize(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        name = '_{0}'.format(func.__name__)
        if not hasattr(self, name):
            result = func(self, *args, **kwargs)
            setattr(self, name, result)
            return result
        return getattr(self, name)
    return wrapper


def process_values(values):
    return list(map(process_value, values))


def process_value(value):
    if isinstance(value, tuple):
        if len(value) == 2:
            value = {'at': value[0], 'value': value[1]}
        elif len(value) == 1:
            value = {'value': value[0]}
    elif not isinstance(value, dict):
        value = {'value': value}

    # Ensure a datetime in the value, the server will ensure local
    # datetime if no value is passed anyway, but since the server
    # doesn't return the value created, there's no way to get it unless
    # all the values are requested again
    value['at'] = to_iso(value.get('at', datetime.now()))
    return value


def to_iso(dtime):
    if not isinstance(dtime, (date, datetime)):
        dtime = iso8601.parse_date(dtime)
    return dtime.replace(tzinfo=iso8601.UTC)\
                .strftime('%Y-%m-%dT%H:%M:%S.%fZ')
