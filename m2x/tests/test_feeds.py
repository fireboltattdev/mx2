import json

from sure import expect
from httpretty import HTTPretty

from m2x.feeds import Feeds
from m2x.tests.base import TestCase


FEED = {
    'id': '93e16394d432a43ab5c06cfc96fdf399',
    'name': 'Foobar',
    'description': 'Foobar description',
    'visibility': 'public',
    'status': 'active',
    'url': '/feeds/93e16394d432a43ab5c06cfc96fdf399',
    'key': '10bf31f303b9460418ff8ffce3524dc2',
    'location': {},
    'streams': [],
    'created': '2013-10-11T05:38:28Z',
    'updated': '2013-10-11T05:38:28Z'
}

FEEDS = {
    'feeds': [{
        'id': '93e16394d432a43ab5c06cfc96fdf399',
        'name': 'Foobar1',
        'description': 'Foobar1 description',
        'visibility': 'public',
        'status': 'active',
        'url': '/feeds/93e16394d432a43ab5c06cfc96fdf399',
        'key': '10bf31f303b9460418ff8ffce3524dc2',
        'location': {},
        'streams': [],
        'created': '2013-10-11T05:38:28Z',
        'updated': '2013-10-11T05:38:28Z'
    }, {
        'id': '1d2bb2c40babd2fc6342925014e0ced7',
        'name': 'Foobar2',
        'description': 'Foobar2 description',
        'visibility': 'public',
        'status': 'active',
        'url': '/feeds/1d2bb2c40babd2fc6342925014e0ced7',
        'key': '6f8499eb97b33e7de6185964dfa89382',
        'location': {},
        'streams': [],
        'created': '2013-10-11T05:41:44Z',
        'updated': '2013-10-11T05:41:44Z'
    }],
    'total': 2,
    'pages': 1,
    'limit': 10,
    'current_page': 1
}


class FeedsTestCase(TestCase):
    def setUp(self):
        super(FeedsTestCase, self).setUp()
        HTTPretty.register_uri(HTTPretty.GET, self._url(Feeds.PATH),
                               status=200, body=json.dumps(FEEDS))


class TestFeeds(FeedsTestCase):
    def test_list(self):
        feeds = self.client.feeds
        expect(len(feeds)).to.equal(2)
        expect(feeds[0].data['name']).to.equal('Foobar1')
        expect(feeds[1].data['name']).to.equal('Foobar2')

    def test_create(self):
        self.client.feeds.create.when.called_with(
            name='Name',
            description='Description',
            visibility='private'
        ).should.throw(NotImplementedError)

    def test_details(self):
        url = self._url(self.client.feeds.item_path(
            '93e16394d432a43ab5c06cfc96fdf399'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(FEED),
                               content_type='application/json')
        feed = self.client.feeds.details(
            '93e16394d432a43ab5c06cfc96fdf399'
        )
        expect(feed.data['name']).to.equal('Foobar')
        expect(feed.name).to.equal('Foobar')
        expect(feed.data['description']).to.equal('Foobar description')
        expect(feed.description).to.equal('Foobar description')
        expect(feed.data['visibility']).to.equal('public')
        expect(feed.visibility).to.equal('public')


class TestFeed(FeedsTestCase):
    def test_update(self):
        url = self._url(self.client.feeds.item_path(
            '93e16394d432a43ab5c06cfc96fdf399'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(FEED),
                               content_type='application/json')
        feed = self.client.feeds.details('93e16394d432a43ab5c06cfc96fdf399')
        feed.update.when.called_with(
            name='Name',
            description='Description',
            visibility='private'
        ).should.throw(NotImplementedError)

    def test_remove(self):
        url = self._url(self.client.feeds.item_path(
            '93e16394d432a43ab5c06cfc96fdf399'
        ))
        HTTPretty.register_uri(HTTPretty.GET, url, status=200,
                               body=json.dumps(FEED),
                               content_type='application/json')
        feed = self.client.feeds.details('93e16394d432a43ab5c06cfc96fdf399')
        feed.remove.when.called_with().should.throw(NotImplementedError)
