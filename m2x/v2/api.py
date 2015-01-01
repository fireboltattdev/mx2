from m2x.utils import pmemoize
from m2x.api import APIBase
from m2x.v2.devices import Devices, Catalog
from m2x.v2.distributions import Distributions
from m2x.v2.keys import Keys


class APIVersion2(APIBase):
    PATH = '/v2'

    @pmemoize
    def devices(self):
        return Devices(self)

    @pmemoize
    def catalog(self):
        return Catalog(self)

    @pmemoize
    def distributions(self):
        return Distributions(self)

    @pmemoize
    def keys(self):
        return Keys(self)
