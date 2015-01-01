from m2x.utils import memoize

from m2x.api import APIBase
from m2x.v1.batches import Batches
from m2x.v1.blueprints import Blueprints
from m2x.v1.datasources import DataSources
from m2x.v1.feeds import Feeds
from m2x.v1.keys import Keys


class APIVersion1(APIBase):
    PATH = '/v1'

    @property
    @memoize
    def blueprints(self):
        return Blueprints(self)

    @property
    @memoize
    def batches(self):
        return Batches(self)

    @property
    @memoize
    def datasources(self):
        return DataSources(self)

    @property
    @memoize
    def feeds(self):
        return Feeds(self)

    @property
    @memoize
    def keys(self):
        return Keys(self)
