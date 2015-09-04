from m2x.v2.resource import Resource

class Chart(Resource):
    COLLECTION_PATH = 'charts'
    ITEM_PATH = 'charts/{id}'
    ITEMS_KEY = 'charts'