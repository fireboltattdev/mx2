import hashlib
import unittest

from httpretty import HTTPretty

from m2x.client import M2XClient


API_KEY = hashlib.md5('python-m2x'.encode('utf8')).hexdigest()


class TestCase(unittest.TestCase):
    API_VERSION = None

    def setUp(self):
        self.client = M2XClient(key=API_KEY, api=self.API_VERSION)
        HTTPretty.enable()

    def tearDown(self):
        self.client = None
        HTTPretty.disable()

    def _url(self, path):
        return self.client.api.url(path)
