from m2x.v1.resource import Collection, Item
from m2x.v1.feeds import HasFeedMixin


class Blueprint(Item, HasFeedMixin):
    PATH = 'blueprints/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']


class Blueprints(Collection):
    PATH = 'blueprints'
    ITEMS_KEY = 'blueprints'
    ITEM_CLASS = Blueprint
