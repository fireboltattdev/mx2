from m2x.feeds import HasFeedMixin
from m2x.resource import Collection, Item


class DataSource(Item, HasFeedMixin):
    PATH = 'datasources/{id}'


class DataSources(Collection):
    PATH = 'datasources'
    ITEMS_KEY = 'datasources'
    ITEM_CLASS = DataSource
