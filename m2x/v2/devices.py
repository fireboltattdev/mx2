from m2x.utils import pmemoize
from m2x.resource import Collection, Item
from m2x.v2.streams import Streams
from m2x.v2.triggers import Triggers


class Device(Item):
    PATH = 'devices/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']

    @pmemoize
    def streams(self):
        return Streams(self.api, device_id=self.id)

    @pmemoize
    def location(self, **location):
        if not self.data.get('location'):
            self.data['location'] = self.api.get(
                self.path(self.PATH + '/location')
            )
        return self.data['location']

    @pmemoize
    def update_location(self, **location):
        self.api.post(self.path(self.PATH + '/location'),
                      data=location)
        self.data['location'] = location
        return location

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
