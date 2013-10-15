from requests import session

from m2x import version


USERAGENT = 'python-m2x/{0}'.format(version)


class APIBase(object):
    PATH = '/'

    def __init__(self, key, client):
        self.key = key
        self.client = client
        self.session = self._session()

    def request(self, *args, **kwargs):
        return self.session.request(*args, **kwargs)

    def _session(self):
        sess = session()
        sess.headers.update({'X-M2X-KEY': self.key,
                             'Content-type': 'application/json',
                             'User-Agent': USERAGENT})
        return sess

    def url(self, *parts):
        return self.client.url(self.PATH, *parts)


class APIVersion1(APIBase):
    PATH = '/v1'
