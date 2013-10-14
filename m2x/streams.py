from .resource import Collection
from .values import Value


class Stream(Collection):
    path = 'feeds/{feed_id}/streams/{name}'
    items_key = 'values'
    item_class = Value

    def __init__(self, feed_id, *args, **kwargs):
        super(Stream, self).__init__(*args, **kwargs)
        self.feed_id = feed_id
        self.data['feed_id'] = feed_id

    def values(self):
        return self.itemize(self.get(self._path(self.path + '/values')))

    def add_value(self, **attrs):
        return self.put(self._path(), data=attrs)


class Streams(Collection):
    path = 'feeds/{feed_id}/streams'
    items_key = 'streams'
    item_class = Stream

    def __init__(self, feed_id, *args, **kwargs):
        super(Streams, self).__init__(*args, **kwargs)
        self.feed_id = feed_id
        self.data['feed_id'] = feed_id

    def list(self):
        return self.itemize(self.get(self._path()))

    def create(self, name, **attrs):
        return self.post(Stream.path.format(feed_id=self.feed_id, name=name),
                         data=attrs)

    def details(self, name):
        return self.item(self.get(Stream.path.format(feed_id=self.feed_id,
                                                     name=name)))

    def item(self, entry):
        return self.item_class(self.feed_id, api=self.api, data=entry)
