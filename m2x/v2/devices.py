from m2x.resource import Collection, Item


class Device(Item):
    PATH = 'devices/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']


class Devices(Collection):
    PATH = 'devices'
    ITEMS_KEY = 'devices'
    ITEM_CLASS = Device
