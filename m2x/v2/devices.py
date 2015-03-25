from m2x.v2.resource import Resource
from m2x.v2.streams import Stream
from m2x.v2.triggers import Trigger
from m2x.v2.keys import Key


class Device(Resource):
    COLLECTION_PATH = 'devices'
    ITEM_PATH = 'devices/{id}'
    ITEMS_KEY = 'devices'

    def streams(self):
        return Stream.list(self.api, self)

    def stream(self, name):
        return Stream.get(self.api, self, name)

    def create_stream(self, name, **params):
        return Stream.create(self.api, self, name, **params)

    def update_stream(self, name, **params):
        return Stream.item_update(self.api, self, name, **params)

    def keys(self):
        return Key.list(self.api, device=self.id)

    def create_key(self, **params):
        return Key.create(self.api, device=self.id, **params)

    def location(self, **location):
        location = self.data.get('location')
        if not location:
            data = self.api.get(self.subpath('/location')) or {}
            location = data.get('location')
        return location

    def update_location(self, **params):
        return self.api.put(self.subpath('/location'), data=params)

    def log(self):
        return self.api.get(self.subpath('/log'))

    def triggers(self, **params):
        return Trigger.list(self.api, self, **params)

    def create_trigger(self, **params):
        return Trigger.create(self.api, self, **params)

    def post_updates(self, **values):
        return self.api.post(self.subpath('/updates'), data=values)

    @classmethod
    def by_tags(cls, api):
        response = api.get('devices/tags') or {}
        return response.get('tags') or []

    @classmethod
    def catalog(cls, api, **params):
        response = api.get('devices/catalog', **params)
        return cls.itemize(api, response)
