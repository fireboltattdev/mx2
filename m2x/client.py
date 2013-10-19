from m2x.api import APIVersion1
from m2x.batches import Batches
from m2x.blueprints import Blueprints
from m2x.datasources import DataSources
from m2x.feeds import Feeds
from m2x.keys import Keys
from m2x.utils import memoize


class M2XClient(object):
    ENDPOINT = 'https://api-m2x.att.com'

    def __init__(self, key, api=APIVersion1, endpoint=None):
        self.endpoint = endpoint or self.ENDPOINT
        self.api = api(key, self)

    def url(self, *parts):
        return '/'.join([part.strip('/') for part in (self.endpoint,) + parts
                            if part])

    @property
    @memoize
    def blueprints(self):
        return Blueprints(self.api)

    @property
    @memoize
    def batches(self):
        return Batches(self.api)

    @property
    @memoize
    def datasources(self):
        return DataSources(self.api)

    @property
    @memoize
    def feeds(self):
        return Feeds(self.api)

    @property
    @memoize
    def keys(self):
        return Keys(self.api)
