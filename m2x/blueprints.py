from .resource import Collection, Item


class Blueprint(Item):
    path = 'blueprints/{id}'

    def create_batch(self, **attrs):
        return self.post(self._path(self.path + '/batches'), data=attrs)


class Blueprints(Collection):
    path = 'blueprints'
    items_key = 'blueprints'
    item_class = Blueprint
