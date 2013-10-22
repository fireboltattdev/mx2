from m2x.resource import Collection, Item
from m2x.streams import Streams
from m2x.keys import FeedKeys
from m2x.utils import memoize


class Location(Item):
    PATH = 'feeds/{feed_id}/location'


class Log(Item):
    pass


class Logs(Collection):
    PATH = 'feeds/{feed_id}/log'
    ITEMS_KEY = 'requests'
    ITEM_CLASS = Log


class Feed(Item):
    PATH = 'feeds/{id}'

    def remove(self):
        raise NotImplementedError('API not implemented')

    def update(self, **attrs):
        raise NotImplementedError('API not implemented')

    @property
    @memoize
    def location(self):
        location = self.api.get(self.path(self.PATH + '/location'))
        return Location(self.api, feed_id=self.id, **location)

    @property
    @memoize
    def keys(self):
        return FeedKeys(self.api, feed_id=self.id)

    @property
    @memoize
    def logs(self):
        return Logs(self.api, feed_id=self.id)

    @property
    @memoize
    def streams(self):
        return Streams(self.api, feed_id=self.id)


class Feeds(Collection):
    PATH = 'feeds'
    ITEMS_KEY = 'feeds'
    ITEM_CLASS = Feed

    def create(self, **attrs):
        raise NotImplementedError('Create a feed using Blueprint or '
                                  'DataSources API')
