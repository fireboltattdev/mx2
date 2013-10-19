import json
from requests import HTTPError

from sure import expect
from httpretty import HTTPretty

from m2x.datasources import DataSources
from m2x.tests.base import TestCase


DATASOURCE = {
    'id': '22a250190e33aea711196ff3f80d7a98',
    'name': 'Foobar',
    'description': 'Foobar description',
    'visibility': 'public',
    'status': 'active',
    'feed': '/feeds/22a250190e33aea711196ff3f80d7a98',
    'url': '/datasources/22a250190e33aea711196ff3f80d7a98',
    'key': '7fa99ef9176753841fa5fb7d1ebdaed1',
    'created': '2013-10-15T17:40:55Z',
    'updated': '2013-10-15T17:40:55Z'
}

DATASOURCES = {
    'datasources': [{
        'id': '22a250190e33aea711196ff3f80d7a98',
        'name': 'Foobar1',
        'description': 'Foobar1 description',
        'visibility': 'public',
        'status': 'active',
        'feed': '/feeds/22a250190e33aea711196ff3f80d7a98',
        'url': '/datasources/22a250190e33aea711196ff3f80d7a98',
        'key': '7fa99ef9176753841fa5fb7d1ebdaed1',
        'created': '2013-10-15T17:40:55Z',
        'updated': '2013-10-15T17:40:55Z'
    }, {
        'id': '72df77cdbabc01ffdfa072c884de7185',
        'name': 'Foobar2',
        'description': 'Foobar2 description',
        'visibility': 'public',
        'status': 'active',
        'feed': '/feeds/72df77cdbabc01ffdfa072c884de7185',
        'url': '/datasources/72df77cdbabc01ffdfa072c884de7185',
        'key': '6f08db3dfc3378ee0e274b75ba39ae86',
        'created': '2013-10-15T17:41:23Z',
        'updated': '2013-10-15T17:41:23Z'
    }]
}


class DatasourcesTestCase(TestCase):
    def setUp(self):
        super(DatasourcesTestCase, self).setUp()
        HTTPretty.register_uri(HTTPretty.GET, self._url(DataSources.PATH),
                               status=200, body=json.dumps(DATASOURCES))


class TestDatasources(DatasourcesTestCase):
    def test_list(self):
        datasources = self.client.datasources
        expect(len(datasources)).to.equal(2)
        expect(datasources[0].data['name']).to.equal('Foobar1')
        expect(datasources[1].data['name']).to.equal('Foobar2')

    def test_create(self):
        url = self._url(self.client.datasources.path())
        HTTPretty.register_uri(HTTPretty.POST, url, status=201,
                               body=json.dumps(DATASOURCE),
                               content_type='application/json')
        datasource = self.client.datasources.create(
            name='Foobar', description='Foobar description',
            visibility='public'
        )
        expect(datasource.data['name']).to.equal('Foobar')
        expect(datasource.name).to.equal('Foobar')
        expect(datasource.data['description']).to.equal('Foobar description')
        expect(datasource.description).to.equal('Foobar description')
        expect(datasource.data['visibility']).to.equal('public')
        expect(datasource.visibility).to.equal('public')

    def test_details(self):
        url = self._url(self.client.datasources.item_path(
            id='22a250190e33aea711196ff3f80d7a98'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(DATASOURCE),
                               content_type='application/json')
        datasource = self.client.datasources.details(
            '22a250190e33aea711196ff3f80d7a98'
        )
        expect(datasource.data['name']).to.equal('Foobar')
        expect(datasource.name).to.equal('Foobar')
        expect(datasource.data['description']).to.equal('Foobar description')
        expect(datasource.description).to.equal('Foobar description')
        expect(datasource.data['visibility']).to.equal('public')
        expect(datasource.visibility).to.equal('public')


class TestDatasource(DatasourcesTestCase):
    def test_update(self):
        url = self._url(self.client.datasources.item_path(
            id='22a250190e33aea711196ff3f80d7a98'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(DATASOURCE),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.PUT, url, status=200, body='')
        datasource = self.client.datasources.details(
            '22a250190e33aea711196ff3f80d7a98'
        )
        datasource.update(name='Foobar updated', visibility='private')
        expect(datasource.data['name']).to.equal('Foobar updated')
        expect(datasource.name).to.equal('Foobar updated')
        expect(datasource.data['visibility']).to.equal('private')
        expect(datasource.visibility).to.equal('private')

    def test_remove(self):
        url = self._url(self.client.datasources.item_path(
            id='22a250190e33aea711196ff3f80d7a98'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(DATASOURCE),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.DELETE, url, status=200, body='')
        datasource = self.client.datasources.details(
            '22a250190e33aea711196ff3f80d7a98'
        )
        datasource.remove()
        HTTPretty.register_uri(HTTPretty.GET, url, status=404,
                               content_type='application/json')
        self.client.datasources.details.when.called_with(
            '22a250190e33aea711196ff3f80d7a98'
        ).should.throw(HTTPError)
