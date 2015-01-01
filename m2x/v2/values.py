from datetime import datetime

from m2x.utils import process_value, to_iso
from m2x.resource import Collection, Item


class Value(Item):
    pass


class Values(Collection):
    PATH = 'devices/{device_id}/streams/{stream_name}/values'
    ITEMS_KEY = 'values'
    ITEM_CLASS = Value
    SORT_KEY = 'at'

    def add_value(self, value, at=None):
        at = datetime.now() if at is None else at
        values = self.add_values({'value': value, 'at': at})
        return values[0] if values else None

    def add_values(self, *values):
        values = self.process_values(*values)
        self.api.post(self.path(), data={'values': values})
        values = [self.item(val) for val in values]
        self.extend(values)
        self.order()
        return values

    def by_date(self, start=None, end=None, limit=None):
        params = {}
        if start:
            params['start'] = to_iso(start)
        if end:
            params['end'] = to_iso(end)
        if limit:
            params['limit'] = int(limit)
        return self.search(**params)

    def process_values(self, *values):
        # Supported format for values:
        #   [ (at, value),
        #     value,
        #     {'value': value}
        #     {'at': at, 'value': value} ]
        return [process_value(value) for value in values]
