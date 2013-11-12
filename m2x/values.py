from datetime import date, datetime

from iso8601 import iso8601

from m2x.resource import Collection, Item


class Value(Item):
    pass


class ValuesMixin(object):
    def add_values(self, values):
        values = self.process_values(values)
        self.api.post(self.path(), data={'values': values})
        return values

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

    def process_values(self, values):
        # Supported format for values:
        #   [ (at, value),
        #     value,
        #     {'value': value}
        #     {'at': at, 'value': value} ]
        return [self.process_value(value) for value in values]

    def process_value(self, value):
        if isinstance(value, tuple):
            if len(value) == 2:
                value = {'at': value[0], 'value': value[1]}
            elif len(value) == 1:
                value = {'value': value[0]}
        elif not isinstance(value, dict):
            value = {'value': value}

        # Ensure a datetime in the value, the server will ensure local
        # datetime if no value is passed anyway, but since the server
        # doesn't return the value created, there's no way to get it unless
        # all the values are requested again
        dtime = value.pop('at', datetime.now())
        if dtime:
            if not isinstance(dtime, (date, datetime)):
                try:
                    dtime = iso8601.parse_date(dtime)
                except iso8601.ParseError:
                    dtime = datetime.now()
            value['at'] = dtime.replace(tzinfo=iso8601.UTC)\
                               .strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return value


class Values(Collection, ValuesMixin):
    PATH = 'feeds/{feed_id}/streams/{stream_name}/values'
    ITEMS_KEY = 'values'
    ITEM_CLASS = Value

    def add_value(self, value, at=None):
        values = self.add_values({'value': value, 'at': at})
        return values[0] if values else None

    def add_values(self, *values):
        values = super(Values, self).add_values(values)
        values = [self.item(val) for val in values]
        self.extend(values)
        self.order()
        return values

    def process_values(self, *values):
        return super(Values, self).process_values(values)
