from .resource import Collection, Item


class Batch(Item):
    path = 'batches/{id}'


class Batches(Collection):
    path = 'batches'
    items_key = 'batches'
    item_class = Batch
