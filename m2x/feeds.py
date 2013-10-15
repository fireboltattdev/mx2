from m2x.resource import Collection, Item
from m2x.streams import Stream


class Feed(Item):
    PATH = 'feeds/{id}'

    def location(self):
        return self.get(self.path(self.PATH + '/location'))

    def key(self):
        return self.get('keys', params={'feed': self.data['id']})

    def log(self):
        return self.get(self.path(self.PATH + '/log'))

    def streams(self):
        entries = self.get(self.path(self.PATH + '/streams'))
        return [Stream(self.data['id'], api=self.api, data=entry)
                        for entry in entries['streams']]


class Feeds(Collection):
    PATH = 'feeds'
    ITEMS_KEY = 'feeds'
    ITEM_CLASS = Feed

    def create(self, **attrs):
        return self.put(self.path(), data=attrs)
