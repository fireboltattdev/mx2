import json
from requests import HTTPError

from sure import expect
from httpretty import HTTPretty

from m2x.batches import Batches
from m2x.tests.base import TestCase


BATCHES = {
    'batches': [{
        'id': 'd20588a555a1a3c5404c278154af624a',
        'name': 'Foobar1',
        'description': 'Foobar1 batch description',
        'visibility': 'public',
        'status': 'active',
        'feed': '/feeds/d20588a555a1a3c5404c278154af624a',
        'url': '/batches/d20588a555a1a3c5404c278154af624a',
        'key': '3065a562ec1d8d46667d42e8ba3eb9ea',
        'created': '2013-10-15T17:20:34Z',
        'updated': '2013-10-15T17:20:34Z',
        'datasources': {
            'total': 0,
            'registered': 0,
            'unregistered': 0
        }
    }, {
        'id': 'e18b3c212ead4b435511331bdb61e422',
        'name': 'Foobar2',
        'description': 'Foobar2 batch description',
        'visibility': 'public',
        'status': 'active',
        'feed': '/feeds/e18b3c212ead4b435511331bdb61e422',
        'url': '/batches/e18b3c212ead4b435511331bdb61e422',
        'key': '89cd539c0d40791489e2519e3379d9fc',
        'created': '2013-10-15T17:21:54Z',
        'updated': '2013-10-15T17:21:54Z',
        'datasources': {
            'total': 0,
            'registered': 0,
            'unregistered': 0
        }
    }]
}

BATCH = {
    'id': 'd20588a555a1a3c5404c278154af624a',
    'name': 'Foobar',
    'description': 'Foobar description',
    'visibility': 'public',
    'status': 'active',
    'feed': '/feeds/d20588a555a1a3c5404c278154af624a',
    'url': '/batches/d20588a555a1a3c5404c278154af624a',
    'key': '3065a562ec1d8d46667d42e8ba3eb9ea',
    'created': '2013-10-15T17:20:34Z',
    'updated': '2013-10-15T17:20:34Z',
    'datasources': {
        'total': 0,
        'registered': 0,
        'unregistered': 0
    }
}


class BatchesTestCase(TestCase):
    def setUp(self):
        super(BatchesTestCase, self).setUp()
        HTTPretty.register_uri(HTTPretty.GET, self._url(Batches.PATH),
                               status=200, body=json.dumps(BATCHES))


class TestBatches(BatchesTestCase):
    def test_list(self):
        batches = self.client.batches
        expect(len(batches)).to.equal(2)
        expect(batches[0].data['name']).to.equal('Foobar1')
        expect(batches[1].data['name']).to.equal('Foobar2')

    def test_create(self):
        url = self._url(self.client.batches.path())
        HTTPretty.register_uri(HTTPretty.POST, url, status=201,
                               body=json.dumps(BATCH),
                               content_type='application/json')
        batch = self.client.batches.create(
            name='Foobar', description='Foobar description',
            visibility='public'
        )
        expect(batch.data['name']).to.equal('Foobar')
        expect(batch.name).to.equal('Foobar')
        expect(batch.data['description']).to.equal('Foobar description')
        expect(batch.description).to.equal('Foobar description')
        expect(batch.data['visibility']).to.equal('public')
        expect(batch.visibility).to.equal('public')

    def test_details(self):
        url = self._url(self.client.batches.item_path(
            id='d20588a555a1a3c5404c278154af624a'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(BATCH),
                               content_type='application/json')
        batch = self.client.batches.details('d20588a555a1a3c5404c278154af624a')
        expect(batch.data['name']).to.equal('Foobar')
        expect(batch.name).to.equal('Foobar')
        expect(batch.data['description']).to.equal('Foobar description')
        expect(batch.description).to.equal('Foobar description')
        expect(batch.data['visibility']).to.equal('public')
        expect(batch.visibility).to.equal('public')


class TestBatch(BatchesTestCase):
    def test_update(self):
        url = self._url(self.client.batches.item_path(
            id='d20588a555a1a3c5404c278154af624a'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(BATCH),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.PUT, url, status=200, body='')
        batch = self.client.batches.details('d20588a555a1a3c5404c278154af624a')
        batch.update(name='Foobar updated', visibility='private')
        expect(batch.data['name']).to.equal('Foobar updated')
        expect(batch.name).to.equal('Foobar updated')
        expect(batch.data['visibility']).to.equal('private')
        expect(batch.visibility).to.equal('private')

    def test_remove(self):
        url = self._url(self.client.batches.item_path(
            id='d20588a555a1a3c5404c278154af624a'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(BATCH),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.DELETE, url, status=200, body='')
        batch = self.client.batches.details('d20588a555a1a3c5404c278154af624a')
        batch.remove()
        HTTPretty.register_uri(HTTPretty.GET, url, status=404,
                               content_type='application/json')
        self.client.batches.details.when.called_with(
            'd20588a555a1a3c5404c278154af624a'
        ).should.throw(HTTPError)
