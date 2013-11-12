from m2x.utils import memoize
from m2x.feeds import HasFeedMixin
from m2x.resource import Collection, Item
from m2x.datasources import BatchDataSources


class Batch(Item, HasFeedMixin):
    PATH = 'batches/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']

    @property
    @memoize
    def datasources(self):
        return BatchDataSources(self.api, batch_id=self.id)


class Batches(Collection):
    PATH = 'batches'
    ITEMS_KEY = 'batches'
    ITEM_CLASS = Batch
