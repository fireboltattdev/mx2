from .resource import Collection
from .values import Value


class Stream(Collection):
    PATH = 'feeds/{feed_id}/streams/{name}'
    ITEMS_KEY = 'values'
    ITEM_CLASS = Value

    def __init__(self, feed_id, *args, **kwargs):
        super(Stream, self).__init__(*args, **kwargs)
        self.feed_id = feed_id
        self.data['feed_id'] = feed_id

    def values(self):
        return self.itemize(self.get(self.path(self.PATH + '/values')))

    def add_value(self, **attrs):
        return self.put(self.path(), data=attrs)


class Streams(Collection):
    PATH = 'feeds/{feed_id}/streams'
    ITEMS_KEY = 'streams'
    ITEM_CLASS = Stream

    def __init__(self, feed_id, *args, **kwargs):
        super(Streams, self).__init__(*args, **kwargs)
        self.feed_id = feed_id
        self.data['feed_id'] = feed_id

    def list(self):
        return self.itemize(self.get(self.path()))

    def create(self, name, **attrs):
        return self.post(Stream.PATH.format(feed_id=self.feed_id, name=name),
                         data=attrs)

    def details(self, name):
        return self.item(self.get(Stream.PATH.format(feed_id=self.feed_id,
                                                     name=name)))

    def item(self, entry):
        return self.ITEM_CLASS(self.feed_id, api=self.api, data=entry)
