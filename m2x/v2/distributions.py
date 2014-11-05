from m2x.resource import Collection, Item


class Distribution(Item):
    PATH = 'distributions/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']


class Distributions(Collection):
    PATH = 'distributions'
    ITEMS_KEY = 'distributions'
    ITEM_CLASS = Distribution
