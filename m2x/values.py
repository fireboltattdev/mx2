from m2x.resource import Collection, Item


class Value(Item):
    pass


class Values(Collection):
    PATH = 'feeds/{feed_id}/streams/{stream_name}/values'
    ITEMS_KEY = 'values'
    ITEM_CLASS = Value

    def add_value(self, **attrs):
        path = self.path().rsplit('/', 1)[0]
        return self.put(path, data=attrs)
