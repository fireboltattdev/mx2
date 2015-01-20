import sys
import json
import uuid
import time
import platform
import threading

from requests import session
from paho.mqtt.client import MQTT_ERR_SUCCESS, Client as MQTTClient

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

    def __init__(self, key, client):
        self.apikey = key
        self.client = client
        self._locals = threading.local()

    def url(self, *parts):
        parts = (self.client_endpoint(), self.PATH) + parts
        return '/'.join(map(lambda p: p.strip('/'), filter(None, parts)))

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

    def last_response(self):
        return getattr(self._locals, 'last_response', None)

    def set_last_response(self, response):
        self._locals.last_response = response

    def client_endpoint(self):
        raise NotImplementedError('Implement in subclass')

    def request(self, path, apikey=None, method='GET', **kwargs):
        raise NotImplementedError('Implement in subclass')


class HTTPAPIBase(APIBase):
    @property
    def session(self):
        if not hasattr(self, '_session'):
            sess = session()
            sess.headers.update({'X-M2X-KEY': self.apikey,
                                 'Content-type': 'application/json',
                                 'Accept-Encoding': 'gzip, deflate',
                                 'User-Agent': USER_AGENT})
            self._session = sess
        return self._session

    def client_endpoint(self):
        return self.client.endpoint

    def request(self, path, apikey=None, method='GET', **kwargs):
        url = self.url(path)

        if apikey:
            kwargs.setdefault('headers', {})
            kwargs['headers']['X-M2X-KEY'] = apikey

        if method in ('PUT', 'POST', 'DELETE', 'PATCH') and kwargs.get('data'):
            kwargs['data'] = json.dumps(kwargs['data'])

        resp = self.session.request(method, url, **kwargs)
        self.set_last_response(resp)

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


class MQTTAPIBase(APIBase):
    @property
    def mqtt(self):
        if not hasattr(self, '_mqtt_client'):
            self.responses = {}
            client = MQTTClient()
            client.username_pw_set(self.apikey)
            client.on_connect = self._on_connect
            client.on_message = self._on_message
            client.connect(self.client_endpoint().replace('mqtt://', ''))
            self._mqtt_client = client
            self._mqtt_client.loop_start()
        return self._mqtt_client

    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe('m2x/{apikey}/responses'.format(apikey=self.apikey))

    def _on_message(self, client, userdata, msg):
        msg = json.loads(msg.payload)
        self.responses[msg['id']] = msg

    def client_endpoint(self):
        return self.client.mqtt_endpoint

    def url(self, *parts):
        parts = (self.PATH,) + parts
        return '/{0}'.format('/'.join(map(lambda p: p.strip('/'),
                                          filter(None, parts))))

    def wait_for_response(self, msg_id, timeout=None):
        while msg_id not in self.responses:
            time.sleep(.1)
            if timeout is not None:
                if timeout > 0:
                    timeout -= 1
                else:
                    break
        if msg_id in self.responses:
            response = self.responses.pop(msg_id)
            self.set_last_response(response)
            if 'body' in response:
                response = response['body']
            return response

    def request(self, path, apikey=None, method='GET', **kwargs):
        msg_id = uuid.uuid4().hex
        msg = json.dumps({
            'id': msg_id,
            'method': method,
            'resource': self.url(path),
            'body': kwargs.get('data') or kwargs.get('params') or {}
        })
        status, mid = self.mqtt.publish('m2x/{apikey}/requests'.format(
            apikey=apikey or self.apikey
        ), payload=msg)
        if status == MQTT_ERR_SUCCESS:
            return self.wait_for_response(msg_id, timeout=50)
