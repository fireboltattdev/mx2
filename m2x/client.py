from m2x.api import APIVersion1
from m2x.batches import Batches
from m2x.blueprints import Blueprints
from m2x.datasources import DataSources
from m2x.feeds import Feeds


class M2XClient(object):
    ENDPOINT = 'https://api-m2x.att.com'

    def __init__(self, key, api=APIVersion1, endpoint=None):
        self.endpoint = endpoint or self.ENDPOINT
        self.api = api(key, self)
        self.blueprints = Blueprints(self.api)
        self.batches = Batches(self.api)
        self.datasources = DataSources(self.api)
        self.feeds = Feeds(self.api)

    def url(self, *parts):
        return '/'.join([part.strip('/') for part in (self.endpoint,) + parts
                            if part])
