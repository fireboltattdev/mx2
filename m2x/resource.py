import re
import json
from datetime import datetime

from requests import HTTPError
from six import string_types, text_type

from m2x.errors import APIError


TIME_FORMAT_RE = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
STRING_TYPES = string_types + (text_type,)


class Resource(object):
    PATH = ''

    def __init__(self, api, data=None):
        self.api = api
        self.raw_data = data or {}
        self.data = self.process_data(self.raw_data)

    def request(self, path, **kwargs):
        url = self.api.url(path)
        if kwargs.get('method') in ('PUT', 'POST'):
            kwargs['data'] = json.dumps(kwargs['data'])
        response = self.api.request(url=url, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError as err:
            if err.response.status_code == 422:
                raise APIError(response)
            else:
                raise
        else:
            try:
                return response.json()
            except ValueError:
                return None

    def get(self, path, **kwargs):
        return self.request(path, method='GET', **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request(path, method='POST', **kwargs)

    def put(self, path, *args, **kwargs):
        return self.request(path, method='PUT', **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.request(path, method='DELETE', **kwargs)

    def path(self, path=None, data=None):
        return (path or self.PATH).format(**(data or self.data or {}))

    def process_data(self, data):
        data_processed = {}
        for name, value in data.items():
            if name in ('created', 'updated') or \
               isinstance(value, STRING_TYPES) and TIME_FORMAT_RE.match(value):
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            data_processed[name] = value
        return data_processed

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError as e:
            raise AttributeError('{0}'.format(e))


class Item(Resource):
    def update(self, **attrs):
        response = self.put(self.path(), data=attrs)
        self.raw_data.update(attrs)
        self.data.update(self.process_data(attrs))
        return response

    def remove(self):
        return self.delete(self.path())


class Collection(Item):
    ITEMS_KEY = None
    ITEM_CLASS = None

    def list(self):
        return self.itemize(self.get(self.path()))

    def create(self, **attrs):
        return self.item(self.post(self.path(), data=attrs))

    def details(self, id):
        return self.item(self.get(self.item_path(id)))

    def item(self, entry):
        return self.ITEM_CLASS(self.api, entry)

    def itemize(self, entries):
        if self.ITEMS_KEY and self.ITEM_CLASS:
            entries = [self.item(entry) for entry in entries[self.ITEMS_KEY]]
        return entries

    def item_path(self, id):
        return self.ITEM_CLASS.PATH.format(id=id)
