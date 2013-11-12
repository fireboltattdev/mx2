from m2x.utils import process_value
from m2x.resource import Collection, Item


class Value(Item):
    pass


class Values(Collection):
    PATH = 'feeds/{feed_id}/streams/{stream_name}/values'
    ITEMS_KEY = 'values'
    ITEM_CLASS = Value

    def add_value(self, value, at=None):
        values = self.add_values({'value': value, 'at': at})
        return values[0] if values else None

    def add_values(self, *values):
        values = self.process_values(*values)
        self.api.post(self.path(), data={'values': values})
        values = [self.item(val) for val in values]
        self.extend(values)
        self.order()
        return values

    def process_values(self, *values):
        # Supported format for values:
        #   [ (at, value),
        #     value,
        #     {'value': value}
        #     {'at': at, 'value': value} ]
        return [process_value(value) for value in values]

    def cmp(self, left, right):
        left_at, right_at = left.data.get('at'), right.data.get('at')
        if left_at and right_at:
            return cmp(left_at, right_at)
        elif left_at:
            return -1
        elif right_at:
            return 1
        else:
            return 0
