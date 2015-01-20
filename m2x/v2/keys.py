from m2x.v2.resource import Resource


class Key(Resource):
    COLLECTION_PATH = 'keys'
    ITEM_PATH = 'keys/{key}'
    ITEMS_KEY = 'keys'
    ID_KEY = 'key'

    def regenerate(self):
        self.data.update(
            self.api.post(self.item_path(self.key) + '/regenerate')
        )
