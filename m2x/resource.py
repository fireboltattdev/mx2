import iso8601

from m2x.utils import tags_to_server


class Resource(object):
    PATH = ''

    def __init__(self, api, **data):
        self.api = api
        self.raw_data = {}
        self.data = {}
        self.set_data(data)

    def path(self, path=None):
        return (path or self.PATH).format(**self.data)

    def process_data(self, data):
        data_processed = {}
        for name, value in data.items():
            value = self.is_time(name, value)
            data_processed[name] = value
        return data_processed

    def set_data(self, value):
        self.raw_data.update(value)
        self.data.update(self.process_data(value))

    def is_time(self, name, value):
        try:
            return iso8601.parse_date(value)
        except iso8601.ParseError:
            return value

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError as err:
            raise AttributeError('{0}'.format(err))


class Item(Resource):
    def update(self, **attrs):
        tags = attrs.get('tags')
        if tags:
            attrs['tags'] = tags_to_server(tags)
        response = self.api.put(self.path(), data=attrs)
        if tags:  # restore original value
            attrs['tags'] = tags
        self.set_data(attrs)
        return response

    def remove(self):
        return self.api.delete(self.path())


class Collection(Resource):
    ITEMS_KEY = None
    ITEM_CLASS = None

    def __init__(self, api, **data):
        self._items = []
        self._loaded = False
        super(Collection, self).__init__(api, **data)

    def reload(self):
        self.clean()
        self.load()

    def clean(self):
        self._items = []
        self._loaded = False

    def load(self):
        if not self._loaded:
            self._loaded = True
            self.extend(self.itemize(self.api.get(self.path())))
            self.order()

    def create(self, **attrs):
        if 'tags' in attrs:
            attrs['tags'] = tags_to_server(attrs['tags'])
        item = self.item(self.api.post(self.path(), data=attrs))
        self.append(item)
        self.order()
        return item

    def details(self, id):
        return self.item(self.api.get(self.item_path(id=id)))

    def search(self, query=None, tags=None, page=None, limit=None, **criteria):
        if query:
            criteria['query'] = query
        if tags:
            if isinstance(tags, (list, tuple)):
                tags = ','.join(tags)
            criteria['tags'] = tags
        if page:
            criteria['page'] = int(page)
        if limit:
            criteria['limit'] = int(limit)
        return self.itemize(self.api.get(self.path(), params=criteria))

    def order(self):
        self._items.sort(cmp=self.cmp)

    def cmp(self, left, right):
        # Return ordering priority of left/right items
        return 0

    def item(self, entry):
        return self.ITEM_CLASS(self.api, **entry)

    def itemize(self, entries):
        if self.ITEMS_KEY and self.ITEM_CLASS:
            entries = [self.item(entry) for entry in entries[self.ITEMS_KEY]]
        return entries

    def item_path(self, **params):
        return self.ITEM_CLASS.PATH.format(**params)

    ### List methods

    def extend(self, values):
        self.load()
        self._items.extend(values)

    def append(self, value):
        self.load()
        self._items.append(value)

    def index(self, value):
        return self._items.index(value)

    def __contains__(self, value):
        self.load()
        return self._items.__contains__(value)

    def __reduce__(self, *args, **kwargs):
        self.load()
        return self._items.__reduce__(*args, **kwargs)

    def __len__(self):
        self.load()
        return self._items.__len__()

    def __iter__(self):
        self.load()
        return self._items.__iter__()

    def __getslice__(self, *args, **kwargs):
        self.load()
        return self._items.__getslice__(*args, **kwargs)

    def __getitem__(self, idx):
        self.load()
        return self._items.__getitem__(idx)

    def __repr__(self):
        self.load()
        return self._items.__repr__()
