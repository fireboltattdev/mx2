from m2x.resource import Collection, Item
from m2x.v1.feeds import HasFeedMixin


class DataSource(Item, HasFeedMixin):
    PATH = 'datasources/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']


class DataSources(Collection):
    PATH = 'datasources'
    ITEMS_KEY = 'datasources'
    ITEM_CLASS = DataSource


class BatchDataSources(DataSources):
    PATH = 'batches/{batch_id}/datasources'
