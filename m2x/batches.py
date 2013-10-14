from .resource import Collection, Item


class Batch(Item):
    PATH = 'batches/{id}'


class Batches(Collection):
    PATH = 'batches'
    ITEMS_KEY = 'batches'
    ITEM_CLASS = Batch
