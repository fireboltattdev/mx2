from m2x.utils import pmemoize
from m2x.resource import Collection, Item
from m2x.v2.devices import Devices
from m2x.v2.streams import Streams, Stream
from m2x.v2.triggers import Triggers, Trigger


class DistributionDevices(Devices):
    PATH = 'distributions/{distribution_id}/devices'


class DistributionStream(Stream):
    PATH = 'distributions/{distribution_id}/streams/{name}'


class DistributionStreams(Streams):
    PATH = 'distributions/{distribution_id}/streams'
    ITEM_CLASS = DistributionStream


class DistributionTrigger(Trigger):
    PATH = 'distributions/{distribution_id}/triggers/{id}'


class DistributionTriggers(Triggers):
    PATH = 'distributions/{distribution_id}/triggers'
    ITEM_CLASS = DistributionTrigger


class Distribution(Item):
    PATH = 'distributions/{id}'
    REQUIRED_ON_UPDATE = ['name', 'visibility']

    @pmemoize
    def devices(self):
        return DistributionDevices(self.api, distribution_id=self.id)

    @pmemoize
    def streams(self):
        return DistributionStreams(self.api, distribution_id=self.id)

    @pmemoize
    def triggers(self):
        return DistributionTriggers(self.api, distribution_id=self.id)


class Distributions(Collection):
    PATH = 'distributions'
    ITEMS_KEY = 'distributions'
    ITEM_CLASS = Distribution
