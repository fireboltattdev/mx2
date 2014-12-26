from m2x.utils import memoize
from m2x.api import APIBase
from m2x.v2.devices import Devices
from m2x.v2.distributions import Distributions
from m2x.v2.keys import Keys


class APIVersion2(APIBase):
    PATH = '/v2'

    @property
    @memoize
    def devices(self):
        return Devices(self)

    @property
    @memoize
    def distributions(self):
        return Distributions(self)

    @property
    @memoize
    def keys(self):
        return Keys(self)
