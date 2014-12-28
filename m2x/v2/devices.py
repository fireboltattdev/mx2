from m2x.utils import pmemoize
from m2x.resource import Collection, Item
from m2x.v2.streams import Streams
from m2x.v2.triggers import Triggers


class Location(Item):
    PATH = 'devices/{device_id}/location'


class Device(Item):
    PATH = 'devices/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']

    @pmemoize
    def streams(self):
        return Streams(self.api, device_id=self.id)

    @pmemoize
    def location(self, **location):
        if 'location' in self.data:
            data = self.data
        else:
            data = self.api.get(self.path(self.PATH + '/location')) or {}
        return Location(self.api, device_id=self.id,
                        **data.get('location', {}))

    @pmemoize
    def triggers(self):
        return Triggers(self.api, device_id=self.id)

    def updates(self, **values):
        return self.api.post(self.path(self.PATH + '/updates'),
                             data=values)


class Devices(Collection):
    PATH = 'devices'
    ITEMS_KEY = 'devices'
    ITEM_CLASS = Device

    def groups(self):
        response = self.api.get(self.path(self.PATH + '/groups'))
        if response:
            return response['groups']


class Catalog(Devices):
    PATH = 'devices/catalog'
