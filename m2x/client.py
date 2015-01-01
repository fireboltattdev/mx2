# from m2x.v1.api import APIVersion1
from m2x.v2.api import APIVersion2


class M2XClient(object):
    ENDPOINT = 'http://api-m2x.att.com'

    def __init__(self, key, api=APIVersion2, endpoint=None):
        self.endpoint = endpoint or self.ENDPOINT
        self.api = api(key, self)

    def url(self, *parts):
        return '/'.join([part.strip('/') for part in (self.endpoint,) + parts
                            if part])

    def __getattr__(self, name):
        return getattr(self.api, name)
