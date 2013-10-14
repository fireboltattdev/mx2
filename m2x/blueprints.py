from .resource import Collection, Item


class Blueprint(Item):
    PATH = 'blueprints/{id}'

    def create_batch(self, **attrs):
        return self.post(self.path(self.PATH + '/batches'), data=attrs)


class Blueprints(Collection):
    PATH = 'blueprints'
    ITEMS_KEY = 'blueprints'
    ITEM_CLASS = Blueprint
