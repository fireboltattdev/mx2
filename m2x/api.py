import sys
import json
import platform
import threading

from requests import session

from m2x import version
from m2x.errors import APIError, InactiveAccountError


PYTHON_VERSION = '{major}.{minor}.{micro}'.format(
    major=sys.version_info.major,
    minor=sys.version_info.minor,
    micro=sys.version_info.micro
)

USER_AGENT = 'M2X-Python/{version} python/{python_version} ({platform})'\
                .format(version=version,
                        python_version=PYTHON_VERSION,
                        platform=platform.platform())


class APIBase(object):
    PATH = '/'
    DEFAULT_LIMIT = 256

    def __init__(self, key, client):
        self.apikey = key
        self.client = client
        self.session = self._session()
        self._locals = threading.local()

    def get(self, path, **kwargs):
        return self.request(path, **kwargs)

    def post(self, path, **kwargs):
        return self.request(path, method='POST', **kwargs)

    def put(self, path, **kwargs):
        return self.request(path, method='PUT', **kwargs)

    def delete(self, path, **kwargs):
        return self.request(path, method='DELETE', **kwargs)

    def patch(self, path, **kwargs):
        return self.request(path, method='PATCH', **kwargs)

    def head(self, path, **kwargs):
        return self.request(path, method='HEAD', **kwargs)

    def options(self, path, **kwargs):
        return self.request(path, method='OPTIONS', **kwargs)

    def _session(self):
        sess = session()
        sess.headers.update({'X-M2X-KEY': self.apikey,
                             'Content-type': 'application/json',
                             'Accept-Encoding': 'gzip, deflate',
                             'User-Agent': USER_AGENT})
        return sess

    def url(self, *parts):
        return self.client.url(self.PATH, *parts)

    def last_response(self):
        return self._locals.last_response

    def request(self, path, apikey=None, method='GET', **kwargs):
        url = self.url(path)

        if apikey:
            kwargs.setdefault('headers', {})
            kwargs['headers']['X-M2X-KEY'] = apikey

        if method in ('PUT', 'POST', 'DELETE', 'PATCH') and kwargs.get('data'):
            kwargs['data'] = json.dumps(kwargs['data'])

        resp = self.session.request(method, url, **kwargs)
        self._locals.last_response = resp

        if resp.status_code == 422:
            raise APIError(resp)
        elif resp.status_code == 403:
            raise InactiveAccountError(resp)
        elif resp.status_code == 204:
            return None
        else:
            resp.raise_for_status()
            try:
                return resp.json()
            except ValueError:
                return resp
