from m2x.utils import memoize
from m2x.resource import Collection, Item
from m2x.v2.streams import Streams


class Device(Item):
    PATH = 'devices/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']

    @property
    @memoize
    def streams(self):
        return Streams(self.api, device_id=self.id)


class Devices(Collection):
    PATH = 'devices'
    ITEMS_KEY = 'devices'
    ITEM_CLASS = Device
