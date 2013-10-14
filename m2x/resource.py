import json


class Resource(object):
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

    def _path(self, path=None, data=None):
        return (path or self.path).format(**(data or self.data or {}))


class Item(Resource):
    path = ''

    def update(self, **attrs):
        return self.put(self._path(), data=attrs)

    def remove(self):
        return self.delete(self._path())


class Collection(Item):
    path = ''
    item_class = None
    items_key = None

    def list(self):
        return self.itemize(self.get(self._path()))

    def create(self, **attrs):
        return self.post(self._path(), data=attrs)

    def details(self, id):
        return self.item(self.get(self.item_class.path.format(id=id)))

    def item(self, entry):
        return self.item_class(self.api, entry)

    def itemize(self, entries):
        if self.items_key and self.item_class:
            entries = [self.item(entry) for entry in entries[self.items_key]]
        return entries
