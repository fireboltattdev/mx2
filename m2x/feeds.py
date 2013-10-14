from .resource import Collection, Item
from .streams import Stream


class Feed(Item):
    path = 'feeds/{id}'

    def location(self):
        return self.get(self._path(self.path + '/location'))

    def key(self):
        return self.get('keys', params={'feed': self.data['id']})

    def log(self):
        return self.get(self._path(self.path + '/log'))

    def streams(self):
        entries = self.get(self._path(self.path + '/streams'))
        return [Stream(self.data['id'], api=self.api, data=entry)
                        for entry in entries['streams']]


class Feeds(Collection):
    path = 'feeds'
    items_key = 'feeds'
    item_class = Feed

    def create(self, **attrs):
        return self.put(self._path(), data=attrs)
