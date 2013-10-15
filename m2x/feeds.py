from m2x.resource import Collection, Item
from m2x.streams import Stream


class Feed(Item):
    PATH = 'feeds/{id}'

    def get_location(self):
        return getattr(self, 'location', None) or \
               self.get(self.path(self.PATH + '/location'))

    def get_key(self):
        return self.get('keys', params={'feed': self.data['id']})

    def get_log(self):
        return self.get(self.path(self.PATH + '/log'))

    def get_streams(self):
        entries = self.get(self.path(self.PATH + '/streams'))
        return [Stream(self.data['id'], api=self.api, data=entry)
                        for entry in entries['streams']]


class Feeds(Collection):
    PATH = 'feeds'
    ITEMS_KEY = 'feeds'
    ITEM_CLASS = Feed

    def create(self, **attrs):
        return self.put(self.path(), data=attrs)
