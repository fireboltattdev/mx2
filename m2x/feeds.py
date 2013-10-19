from m2x.resource import Collection, Item
from m2x.streams import Streams
from m2x.keys import FeedKeys


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

    def get_location(self):
        location = self.get(self.path(self.PATH + '/location'))
        return Location(self.api, feed_id=self.id, **location)

    def get_keys(self):
        return FeedKeys(self.api, feed_id=self.id)

    def get_logs(self):
        return Logs(self.api, feed_id=self.id)

    def get_streams(self):
        return Streams(self.api, feed_id=self.id)

    def remove(self):
        raise NotImplementedError('API not implemented')

    def update(self, **attrs):
        raise NotImplementedError('API not implemented')


class Feeds(Collection):
    PATH = 'feeds'
    ITEMS_KEY = 'feeds'
    ITEM_CLASS = Feed

    def create(self, **attrs):
        raise NotImplementedError('API not implemented, create a feed '
                                  'using Blueprint API')
