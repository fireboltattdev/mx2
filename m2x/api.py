from requests import session

from . import version
from .batches import Batches
from .blueprints import Blueprints
from .datasources import DataSources
from .feeds import Feeds


USERAGENT = 'python-m2x/{0}'.format(version)


class APIBase(object):
    path = '/'

    def __init__(self, key, client):
        self.key = key
        self.client = client
        self.session = self._session()
        self.batches = Batches(self)
        self.blueprints = Blueprints(self)
        self.datasources = DataSources(self)
        self.feeds = Feeds(self)

    def request(self, *args, **kwargs):
        return self.session.request(*args, **kwargs)

    def _session(self):
        sess = session()
        sess.headers.update({'X-M2X-KEY': self.key,
                             'User-Agent': USERAGENT})
        return sess

    def url(self, *parts):
        return self.client.url(self.path, *parts)


class APIVersion1(APIBase):
    path = '/v1'
