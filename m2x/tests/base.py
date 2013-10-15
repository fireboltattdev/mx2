import unittest

from httpretty import HTTPretty

from m2x.client import M2XClient


class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = M2XClient(key='foobar', endpoint='http://foobar.com')
        HTTPretty.enable()

    def tearDown(self):
        self.client = None
        HTTPretty.disable()

    def _url(self, path):
        return self.client.api.url(path)
