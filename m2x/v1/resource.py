from m2x.utils import attrs_to_server, attrs_from_server, tags_to_server


class Resource(object):
    PATH = ''

    def __init__(self, api, **data):
        self.api = api
        self.raw_data = {}
        self.data = {}
        self.set_data(data)

    def path(self, path=None):
        return (path or self.PATH).format(**self.data)

    def set_data(self, value):
        self.raw_data.update(value)
        self.data.update(attrs_from_server(value))

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError as err:
            raise AttributeError('{0}'.format(err))


class Item(Resource):
    REQUIRED_ON_UPDATE = None

    def update(self, **attrs):
        # Fill required values with current values to avoid repeating them when
        # using the API
        for name in self.REQUIRED_ON_UPDATE or []:
            if name not in attrs:
                attrs[name] = self.data.get(name)

        attrs = attrs_to_server(attrs)
        response = self.api.put(self.path(), data=attrs)
        self.set_data(attrs_from_server(response or attrs))
        return response

    def remove(self):
        return self.api.delete(self.path())


class Collection(Resource, list):
    ITEMS_KEY = None
    ITEM_CLASS = None
    SORT_KEY = 'updated'
    ID_KEY = 'id'
    DEFAULT_LIMIT = 256

    def reload(self):
        self[:] = []
        self._loaded = False
        self.load()

    def load(self):
        if getattr(self, '_loaded', False):
            return

        self._loaded = True
        response = self.api.get(self.path())
        self[:] = self.itemize(response)

        # Ensure that all the items in the collection are loaded
        # TODO: improve this to avoid hitting the server multiple times
        if 'pages' in response and 'current_page' in response and \
           response['pages'] > response['current_page']:
            for i in range(2, response['pages'] + 1):
                response = self.api.get(self.path(), params={
                    'page': i
                })
                self.extend(self.itemize(response))
        self.sort(key=self.sort_key)

    def create(self, **attrs):
        attrs = attrs_to_server(attrs)
        item = self.item(self.api.post(self.path(), data=attrs))
        self.append(item)
        self.sort(key=self.sort_key)
        return item

    def get(self, id):
        return self.item(self.api.get(self.item_path(**{self.ID_KEY: id})))
    details = get

    def search(self, query=None, tags=None, page=None, limit=None, **criteria):
        criteria['limit'] = self.DEFAULT_LIMIT if limit is None else int(limit)

        if query:
            criteria['q'] = query
            criteria['query'] = query

        if tags:
            criteria['tags'] = tags_to_server(tags)

        if page:
            criteria['page'] = int(page)

        return self.itemize(self.api.get(self.path(), params=criteria))

    def sort_key(self, value):
        return value.data.get(self.SORT_KEY)

    def item(self, entry):
        return self.ITEM_CLASS(self.api, **attrs_from_server(entry))

    def itemize(self, entries):
        if self.ITEMS_KEY and self.ITEM_CLASS:
            entries = [self.item(entry) for entry in entries[self.ITEMS_KEY]]
        return entries

    def item_path(self, **params):
        return self.ITEM_CLASS.PATH.format(**params)

    def __add__(self, *args, **kwargs):
        self.load()
        return list.__add__(self, *args, **kwargs)

    def __contains__(self, *args, **kwargs):
        self.load()
        return list.__contains__(self, *args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        self.load()
        return list.__delitem__(self, *args, **kwargs)

    def __delslice__(self, *args, **kwargs):
        self.load()
        return list.__delslice__(self, *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        self.load()
        return list.__eq__(self, *args, **kwargs)

    def __format__(self, *args, **kwargs):
        self.load()
        return list.__format__(self, *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        self.load()
        return list.__ge__(self, *args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        self.load()
        return list.__getitem__(self, *args, **kwargs)

    def __getslice__(self, *args, **kwargs):
        self.load()
        return list.__getslice__(self, *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        self.load()
        return list.__gt__(self, *args, **kwargs)

    def __hash__(self, *args, **kwargs):
        self.load()
        return list.__hash__(self, *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        self.load()
        return list.__iadd__(self, *args, **kwargs)

    def __imul__(self, *args, **kwargs):
        self.load()
        return list.__imul__(self, *args, **kwargs)

    def __iter__(self, *args, **kwargs):
        self.load()
        return list.__iter__(self, *args, **kwargs)

    def __le__(self, *args, **kwargs):
        self.load()
        return list.__le__(self, *args, **kwargs)

    def __len__(self, *args, **kwargs):
        self.load()
        return list.__len__(self, *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        self.load()
        return list.__lt__(self, *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        self.load()
        return list.__mul__(self, *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        self.load()
        return list.__ne__(self, *args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        self.load()
        return list.__reduce__(self, *args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        self.load()
        return list.__reduce_ex__(self, *args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        self.load()
        return list.__reversed__(self, *args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        self.load()
        return list.__rmul__(self, *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        self.load()
        return list.__setitem__(self, *args, **kwargs)

    def __setslice__(self, *args, **kwargs):
        self.load()
        return list.__setslice__(self, *args, **kwargs)

    def count(self, *args, **kwargs):
        self.load()
        return list.count(self, *args, **kwargs)

    def index(self, *args, **kwargs):
        self.load()
        return list.index(self, *args, **kwargs)

    def insert(self, *args, **kwargs):
        self.load()
        return list.insert(self, *args, **kwargs)

    def pop(self, *args, **kwargs):
        self.load()
        return list.pop(self, *args, **kwargs)

    def remove(self, *args, **kwargs):
        self.load()
        return list.remove(self, *args, **kwargs)

    def reverse(self, *args, **kwargs):
        self.load()
        return list.reverse(self, *args, **kwargs)
