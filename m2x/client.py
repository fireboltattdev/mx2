from .api import APIVersion1


class M2XClient(object):
    ENDPOINT = 'https://api-m2x.att.com'

    def __init__(self, key, api=APIVersion1, endpoint=None):
        self.endpoint = endpoint or self.ENDPOINT
        self.api = api(key, self)

    def url(self, *parts):
        return '/'.join([part.strip('/') for part in (self.endpoint,) + parts
                            if part])
