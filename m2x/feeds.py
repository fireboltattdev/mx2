from m2x.resource import Collection, Item
from m2x.streams import Streams
from m2x.keys import FeedKeys
from m2x.utils import memoize, process_values


class Location(Item):
    PATH = 'feeds/{feed_id}/location'

    def remove(self):
        raise NotImplementedError('API not implemented')


class Log(Item):
    def update(self, **attrs):
        raise NotImplementedError('API not implemented')

    def remove(self):
        raise NotImplementedError('API not implemented')


class Logs(Collection):
    PATH = 'feeds/{feed_id}/log'
    ITEMS_KEY = 'requests'
    ITEM_CLASS = Log

    def create(self, **attrs):
        raise NotImplementedError('API not implemented')


class Feed(Item):
    PATH = 'feeds/{id}'

    def remove(self):
        raise NotImplementedError('API not implemented')

    def update(self, **attrs):
        raise NotImplementedError('API not implemented')

    def add_values(self, values, location=None):
        data = {
            'values': dict((stream, process_values(stream_values))
                                for stream, stream_values in values.items()
            )
        }
        if location is not None:
            data['location'] = location
        self.api.post(self.path(), data=data)
        return data

    @property
    @memoize
    def location(self):
        location = self.api.get(self.path(self.PATH + '/location')) or {}
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

    def search(self, type=None, serial=None, latitude=None, longitude=None,
               distance=None, distance_unit=None, **criteria):
        if type and type in ('blueprint', 'batch', 'datasource'):
            criteria['type'] = type
        if serial:
            criteria['serial'] = serial
        if latitude:
            criteria['latitude'] = latitude
        if longitude:
            criteria['longitude'] = longitude
        if distance and distance_unit in ('mi', 'miles', 'km'):
            criteria['distance'] = distance
            criteria['distance_unit'] = distance_unit
        return super(Feeds, self).search(self, **criteria)


class HasFeedMixin(object):
    FEED_URL_KEY = 'feed'

    @property
    @memoize
    def feed(self):
        return Feed(self.api, **self.api.get(self.data[self.FEED_URL_KEY]))
