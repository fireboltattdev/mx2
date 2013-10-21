from requests import session

from m2x import version


USERAGENT = 'python-m2x/{0}'.format(version)


class APIBase(object):
    PATH = '/'

    def __init__(self, key, client):
        self.key = key
        self.client = client
        self.session = self._session()

    def request(self, **kwargs):
        apikey = kwargs.pop('apikey', None)
        if apikey:
            kwargs.setdefault('headers', {})
            kwargs['headers']['X-M2X-KEY'] = apikey
        return self.session.request(**kwargs)

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
