import json

from requests import session

from m2x import version
from m2x.errors import APIError


USERAGENT = 'python-m2x/{0}'.format(version)


class APIBase(object):
    PATH = '/'

    def __init__(self, key, client):
        self.key = key
        self.client = client
        self.session = self._session()

    def request(self, path, apikey=None, method='GET', **kwargs):
        url = self.url(path)

        if apikey:
            kwargs.setdefault('headers', {})
            kwargs['headers']['X-M2X-KEY'] = apikey

        if method in ('PUT', 'POST') and kwargs.get('data'):
            kwargs['data'] = json.dumps(kwargs['data'])

        response = self.session.request(method, url, **kwargs)
        if response.status_code == 422:
            raise APIError(response)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            pass

    def get(self, path, **kwargs):
        return self.request(path, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request(path, method='POST', **kwargs)

    def put(self, path, *args, **kwargs):
        return self.request(path, method='PUT', **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.request(path, method='DELETE', **kwargs)

    def _session(self):
        sess = session()
        sess.headers.update({'X-M2X-KEY': self.key,
                             'Content-type': 'application/json',
                             'Accept-Encoding': 'gzip, deflate',
                             'User-Agent': USERAGENT})
        return sess

    def url(self, *parts):
        return self.client.url(self.PATH, *parts)
