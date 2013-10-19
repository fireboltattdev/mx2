import json
from requests import HTTPError

from sure import expect
from httpretty import HTTPretty

from m2x.streams import Streams
from m2x.tests.base import TestCase


STREAM = {
    'updated': '2013-10-19T16:17:19Z',
    'name': 'foobar',
    'min': '0.0',
    'url': '/feeds/7cc8f518983dd62254b98d976400a3d4/streams/foobar',
    'max': '32.0',
    'created': '2013-10-19T15:42:38Z',
    'value': '32',
    'id': '4',
    'unit': {
        'symbol': None,
        'label': None
    }
}

STREAMS = {
    'streams': [{
        'updated': '2013-10-19T16:17:19Z',
        'name': 'foobar1',
        'min': '0.0',
        'url': '/feeds/7cc8f518983dd62254b98d976400a3d4/streams/foobar1',
        'max': '32.0',
        'created': '2013-10-19T15:42:38Z',
        'value': '32',
        'id': '4',
        'unit': {
            'symbol': None,
            'label': None
        }
    }, {
        'updated': '2013-10-19T16:17:19Z',
        'name': 'foobar2',
        'min': '0.0',
        'url': '/feeds/7cc8f518983dd62254b98d976400a3d4/streams/foobar2',
        'max': '32.0',
        'created': '2013-10-19T15:42:38Z',
        'value': '32',
        'id': '4',
        'unit': {
            'symbol': None,
            'label': None
        }
    }]
}

FEED_ID = '93e16394d432a43ab5c06cfc96fdf399'


class StreamsTestCase(TestCase):
    def setUp(self):
        super(StreamsTestCase, self).setUp()
        HTTPretty.register_uri(HTTPretty.GET, self.streams_url(),
                               status=200, body=json.dumps(STREAMS))
        self.streams = Streams(api=self.client.api, feed_id=FEED_ID)

    def streams_url(self, **params):
        return self._url(Streams.PATH.format(feed_id=FEED_ID, **params))


class TestStreams(StreamsTestCase):
    def test_list(self):
        expect(len(self.streams)).to.equal(2)
        expect(self.streams[0].data['name']).to.equal('foobar1')
        expect(self.streams[1].data['name']).to.equal('foobar2')

    def test_create(self):
        url = self._url(self.streams.item_path(name='foobar'))
        HTTPretty.register_uri(HTTPretty.PUT, url, status=201,
                               body=json.dumps(STREAM),
                               content_type='application/json')
        stream = self.streams.create('foobar')
        expect(stream.data['name']).to.equal('foobar')
        expect(stream.name).to.equal('foobar')

    def test_details(self):
        url = self._url(self.streams.item_path(name='foobar'))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(STREAM),
                               content_type='application/json')
        stream = self.streams.details('foobar')
        expect(stream.data['name']).to.equal('foobar')
        expect(stream.name).to.equal('foobar')


class TestStream(StreamsTestCase):
    def test_update(self):
        url = self._url(self.streams.item_path(name='foobar'))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(STREAM),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.PUT, url, status=200, body='')
        stream = self.streams.details('foobar')
        stream.update(unit_label='F', unit_symbol='F')
        expect(stream.data['unit']['label']).to.equal('F')
        expect(stream.unit['label']).to.equal('F')
        expect(stream.data['unit']['symbol']).to.equal('F')
        expect(stream.unit['symbol']).to.equal('F')

    def test_remove(self):
        url = self._url(self.streams.item_path(name='foobar'))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(STREAM),
                               content_type='application/json')
        HTTPretty.register_uri(HTTPretty.DELETE, url, status=200, body='')
        stream = self.streams.details('foobar')
        stream.remove()
        HTTPretty.register_uri(HTTPretty.GET, url, status=404,
                               content_type='application/json')
        self.streams.details.when.called_with('foobar')\
                                 .should.throw(HTTPError)
