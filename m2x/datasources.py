from .resource import Collection, Item


class DataSource(Item):
    path = 'datasources/{id}'


class DataSources(Collection):
    path = 'datasources'
    items_key = 'datasources'
    item_class = DataSource
