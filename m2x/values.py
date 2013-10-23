from datetime import date, datetime

from iso8601 import iso8601

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

    def process_values(self, *values):
        # Supported format for values:
        #   [ (at, value),
        #     value,
        #     {'value': value}
        #     {'at': at, 'value': value} ]
        out = []
        for val in values:
            if isinstance(val, tuple):
                if len(val) == 2:
                    val = {'at': val[0], 'value': val[1]}
                elif len(val) == 1:
                    val = {'value': val[0]}
            elif not isinstance(val, dict):
                val = {'value': val}

            # Ensure a datetime in the value, the server will ensure local
            # datetime if no value is passed anyway, but since the server
            # doesn't return the value created, there's no way to get it unless
            # all the values are requested again
            dtime = val.pop('at', datetime.now())
            if dtime:
                if isinstance(dtime, (date, datetime)):
                    val['at'] = dtime.replace(tzinfo=iso8601.UTC)\
                                     .strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    try:
                        val['at'] = iso8601.parse_date(dtime)
                    except iso8601.ParseError:
                        pass
            out.append(val)
        return out
