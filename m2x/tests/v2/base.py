import json

from sure import expect
from httpretty import HTTPretty

from m2x.client import M2XClient
from m2x.utils import attrs_from_server
from m2x.v2.api import APIVersion2

from m2x.tests.base import TestCase, API_KEY


class V2TestCase(TestCase):
    API_VERSION = APIVersion2


class V2CollectionTestCase(object):
    COLLECTION = None
    COLLECTION_URL = ''
    COLLECTION_PROPERTY = None
    CLIENT_PROPERTY = None
    NEW_ITEM = None
    NEW_ITEM_RESPONSE = None
    ITEM_URL = ''

    def setUp(self):
        HTTPretty.register_uri(
            HTTPretty.GET,
            self.COLLECTION_URL,
            status=200,
            body=json.dumps(self.COLLECTION),
            content_type='application/json'
        )
        HTTPretty.register_uri(
            HTTPretty.GET,
            self.ITEM_URL,
            status=200,
            body=json.dumps(self.items_raw[0]),
            content_type='application/json'
        )
        HTTPretty.register_uri(
            HTTPretty.POST,
            self.COLLECTION_URL,
            status=200,
            body=json.dumps(self.NEW_ITEM_RESPONSE),
            content_type='application/json'
        )
        super(V2CollectionTestCase, self).setUp()

    def do_test_list(self):
        items = self.collection
        expect(len(items)).to.equal(len(self.items_raw))

    def do_test_reload(self):
        items = self.collection
        items.reload()
        expect(len(items)).to.equal(len(self.items_raw))

    def do_test_create(self):
        item = self.collection.create(**self.NEW_ITEM)
        self.ensure_equals(item, self.NEW_ITEM_RESPONSE)
        expect(len(self.collection)).to.equal(len(self.items_raw) + 1)

    def do_test_get(self):
        item = self.collection.get(self.items_raw[0][self.id_key])
        self.ensure_equals(item, self.items_raw[0])

    def ensure_equals(self, collection_item, json_item):
        json_item = attrs_from_server(json_item)
        for name, value in collection_item.data.items():
            expect(value).to.equal(json_item[name])

    @property
    def collection(self):
        collection = getattr(self.client, self.CLIENT_PROPERTY)
        collection.load()
        return collection

    @property
    def id_key(self):
        return self.collection.ID_KEY

    @property
    def items_raw(self):
        return self.COLLECTION[self.COLLECTION_PROPERTY]


def v2url(path):
    client = M2XClient(key=API_KEY, api=APIVersion2)
    return client.api.url(path)
