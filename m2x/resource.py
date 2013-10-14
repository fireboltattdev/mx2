import json


class Resource(object):
    PATH = ''

    def __init__(self, api, data=None):
        self.api = api
        self.data = data or {}

    def request(self, path, **kwargs):
        url = self.api.url(path)
        if kwargs.get('method') in ('PUT', 'POST'):
            kwargs['data'] = json.dumps(kwargs['data'])
        response = self.api.request(url=url, **kwargs)
        response.raise_for_status()
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


class Item(Resource):
    def update(self, **attrs):
        return self.put(self.path(), data=attrs)

    def remove(self):
        return self.delete(self.path())


class Collection(Item):
    ITEMS_KEY = None
    ITEM_CLASS = None

    def list(self):
        return self.itemize(self.get(self.path()))

    def create(self, **attrs):
        return self.post(self.path(), data=attrs)

    def details(self, id):
        return self.item(self.get(self.ITEM_CLASS.PATH.format(id=id)))

    def item(self, entry):
        return self.ITEM_CLASS(self.api, entry)

    def itemize(self, entries):
        if self.ITEMS_KEY and self.ITEM_CLASS:
            entries = [self.item(entry) for entry in entries[self.ITEMS_KEY]]
        return entries
