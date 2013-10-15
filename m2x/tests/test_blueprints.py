import json
import unittest
from requests import HTTPError

from sure import expect
from httpretty import HTTPretty

from m2x.client import M2XClient


BLUEPRINTS = {
    'blueprints': [
        {
            'id': 'd803c3faf29cfee82bebbebacbf7c504',
            'name': 'Foobar1',
            'description': 'Foobar1 blueprint',
            'visibility': 'private',
            'status': 'active',
            'feed': '/feeds/d803c3faf29cfee82bebbebacbf7c504',
            'url': '/blueprints/d803c3faf29cfee82bebbebacbf7c504',
            'key': '81b269f6418b483689bdafe5d55a3a98',
            'created': '2013-10-11T05:24:52Z',
            'updated': '2013-10-11T05:24:52Z'
        }, {
            'id': 'a045742f5dc2d779177847c5df0d358e',
            'name': 'Foobar2',
            'description': 'Foobar2 blueprint',
            'visibility': 'private',
            'status': 'active',
            'feed': '/feeds/a045742f5dc2d779177847c5df0d358e',
            'url': '/blueprints/a045742f5dc2d779177847c5df0d358e',
            'key': '6f79c31d186e76722f697b663f921cfb',
            'created': '2013-10-11T05:24:23Z',
            'updated': '2013-10-11T05:24:23Z'
        }
    ]
}

BLUEPRINT = {
    'id': '4bd637331de35c6a8344522a1aed317b',
    'name': 'Foobar',
    'description': 'Foobar description',
    'visibility': 'public',
    'status': 'active',
    'feed': '/feeds/4bd637331de35c6a8344522a1aed317b',
    'url': '/blueprints/4bd637331de35c6a8344522a1aed317b',
    'key': '96a77accb547dcc6e8216070f4072d5a',
    'created': '2013-10-14T22:47:16Z',
    'updated': '2013-10-14T22:47:16Z'
}


class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = M2XClient(key='foobar', endpoint='http://foobar.com')
        HTTPretty.enable()

    def tearDown(self):
        self.client = None
        HTTPretty.disable()

    def _url(self, path):
        return self.client.api.url(path)


class TestBlueprints(TestCase):
    def test_list(self):
        url = self._url(self.client.blueprints.path())
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(BLUEPRINTS))
        blueprints = self.client.blueprints.list()
        expect(len(blueprints)).to.equal(2)
        expect(blueprints[0].data['name']).to.equal('Foobar1')
        expect(blueprints[1].data['name']).to.equal('Foobar2')

    def test_create(self):
        url = self._url(self.client.blueprints.path())
        HTTPretty.register_uri(HTTPretty.POST, url, status=201,
                               body=json.dumps(BLUEPRINT),
                               content_type='application/json')
        blueprint = self.client.blueprints.create(
            name='Foobar', description='Foobar description',
            visibility='public'
        )
        expect(blueprint.data['name']).to.equal('Foobar')
        expect(blueprint.data['description']).to.equal('Foobar description')
        expect(blueprint.data['visibility']).to.equal('public')

    def test_details(self):
        url = self._url(self.client.blueprints.item_path(
            '4bd637331de35c6a8344522a1aed317b'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(BLUEPRINT),
                               content_type='application/json')
        blueprint = self.client.blueprints.details(
            '4bd637331de35c6a8344522a1aed317b'
        )
        expect(blueprint.data['name']).to.equal('Foobar')
        expect(blueprint.data['description']).to.equal('Foobar description')
        expect(blueprint.data['visibility']).to.equal('public')


class TestBlueprint(TestCase):
    def test_update(self):
        url = self._url(self.client.blueprints.item_path(
            '4bd637331de35c6a8344522a1aed317b'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(BLUEPRINT),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.PUT, url, status=200, body='')
        blueprint = self.client.blueprints.details(
            '4bd637331de35c6a8344522a1aed317b'
        )
        blueprint.update(name='Foobar updated', visibility='private')
        expect(blueprint.data['name']).to.equal('Foobar updated')
        expect(blueprint.data['visibility']).to.equal('private')

    def test_remove(self):
        url = self._url(self.client.blueprints.item_path(
            '4bd637331de35c6a8344522a1aed317b'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(BLUEPRINT),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.DELETE, url, status=200, body='')
        blueprint = self.client.blueprints.details(
            '4bd637331de35c6a8344522a1aed317b'
        )
        blueprint.remove()
        HTTPretty.register_uri(HTTPretty.GET, url, status=404,
                               content_type='application/json')
        self.client.blueprints.details.when.called_with(
            '4bd637331de35c6a8344522a1aed317b'
        ).should.throw(HTTPError)
