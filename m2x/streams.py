from m2x.resource import Collection, Item
from m2x.values import Values
from m2x.utils import memoize


class Stream(Item):
    PATH = 'feeds/{feed_id}/streams/{name}'

    @property
    @memoize
    def values(self):
        return Values(self.api, feed_id=self.feed_id, stream_name=self.name)


class Streams(Collection):
    PATH = 'feeds/{feed_id}/streams'
    ITEMS_KEY = 'streams'
    ITEM_CLASS = Stream

    def create(self, name, **attrs):
        url = Stream.PATH.format(feed_id=self.feed_id, name=name)
        stream = self.item(self.put(url, data=attrs))
        self.append(stream)
        return stream

    def details(self, name):
        url = Stream.PATH.format(feed_id=self.feed_id, name=name)
        return self.item(self.get(url))

    def item(self, entry):
        return self.ITEM_CLASS(self.api, feed_id=self.feed_id, **entry)
