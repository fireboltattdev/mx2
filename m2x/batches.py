from m2x.feeds import HasFeedMixin
from m2x.resource import Collection, Item


class Batch(Item, HasFeedMixin):
    PATH = 'batches/{id}'


class Batches(Collection):
    PATH = 'batches'
    ITEMS_KEY = 'batches'
    ITEM_CLASS = Batch
