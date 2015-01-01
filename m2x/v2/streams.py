from m2x.utils import pmemoize
from m2x.resource import Collection, Item
from m2x.v2.values import Values


class Sampling(Values):
    PATH = 'devices/{device_id}/streams/{stream_name}/sampling'


class Stream(Item):
    PATH = 'devices/{device_id}/streams/{name}'

    @pmemoize
    def values(self):
        return Values(self.api, device_id=self.device_id,
                      stream_name=self.name)

    @pmemoize
    def sampling(self):
        return Sampling(self.api, device_id=self.device_id,
                        stream_name=self.name)

    def stats(self, **attrs):
        return self.api.get(self.path(self.PATH + '/stats'), data=attrs)


class Streams(Collection):
    PATH = 'devices/{device_id}/streams'
    ITEMS_KEY = 'streams'
    ITEM_CLASS = Stream
    ID_KEY = 'name'

    def create(self, name, **attrs):
        stream = self.ITEM_CLASS(self.api, name=name, **self.data)
        stream.update(**attrs)
        self.append(stream)
        return stream

    def item(self, entry):
        return self.ITEM_CLASS(self.api, device_id=self.device_id, **entry)

    def item_path(self, **params):
        return super(Streams, self).item_path(device_id=self.device_id,
                                              **params)
