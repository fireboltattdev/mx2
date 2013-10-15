from m2x.resource import Collection, Item


class Blueprint(Item):
    PATH = 'blueprints/{id}'


class Blueprints(Collection):
    PATH = 'blueprints'
    ITEMS_KEY = 'blueprints'
    ITEM_CLASS = Blueprint
