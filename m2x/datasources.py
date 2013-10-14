from .resource import Collection, Item


class DataSource(Item):
    PATH = 'datasources/{id}'


class DataSources(Collection):
    PATH = 'datasources'
    ITEMS_KEY = 'datasources'
    ITEM_CLASS = DataSource
