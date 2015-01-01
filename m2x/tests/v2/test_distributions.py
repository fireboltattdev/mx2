# TODO:
#
# 2. Distribution
#   a. item methods (update, remove)
#   b. devices retrieval
#   c. streams retrieval
#   d. triggers retrieval


from m2x.tests.v2.base import V2TestCase, V2CollectionTestCase, v2url


class TestDistributions(V2CollectionTestCase, V2TestCase):
    COLLECTION_URL = v2url('/distributions')
    ITEM_URL = v2url('/distributions/5585477bbaa006bc71a069c7baf46ea6')
    COLLECTION_PROPERTY = 'distributions'
    CLIENT_PROPERTY = 'distributions'
    COLLECTION = {
        'distributions': [{
            'status': 'enabled',
            'created': '2014-09-25T04:16:38.404Z',
            'updated': '2014-09-25T04:16:39.404Z',
            'description': 'My first distribution',
            'url': v2url('/distributions/5585477bbaa006bc71a069c7baf46ea6'),
            'visibility': 'public',
            'key': 'badf8254c7b183e4136d1c6ec6b33fca',
            'devices': {
                'unregistered': 0,
                'registered': 0,
                'total': 0
            },
            'groups': [],
            'serial': None,
            'id': '5585477bbaa006bc71a069c7baf46ea6',
            'name': 'Sample Batch'
        }, {
            'status': 'enabled',
            'updated': '2014-09-25T04:14:06.321Z',
            'description': 'My second distribution',
            'created': '2014-09-25T04:14:05.815Z',
            'url': v2url('/distributions/bfc34d4f364ea9c659808de1f50cb83c'),
            'visibility': 'public',
            'key': '8f9fb842d0adda457efc06569c2eaf51',
            'devices': {
                'unregistered': 0,
                'registered': 0,
                'total': 0
            },
            'groups': [],
            'serial': None,
            'id': 'bfc34d4f364ea9c659808de1f50cb83c',
            'name': 'Sample Batch'
        }],
        'total': 2,
        'limit': 10,
        'pages': 1,
        'current_page': 1
    }
    NEW_ITEM = {
        'status': 'enabled',
        'description': 'Distribution',
        'visibility': 'public',
        'name': 'Sample distribution',
    }
    NEW_ITEM_RESPONSE = {
        'status': 'enabled',
        'updated': '2014-09-27T07:26:18.104Z',
        'description': 'Distribution',
        'created': '2014-09-26T04:16:37.872Z',
        'url': v2url('/distributions/bfc34d4f364ea9c659808de1f50cb834'),
        'visibility': 'public',
        'key': '8f9fb842d0adda457efc06569c2eaf51',
        'devices': {
            'unregistered': 0,
            'registered': 0,
            'total': 0
        },
        'groups': [],
        'serial': None,
        'id': 'bfc34d4f364ea9c659808de1f50cb834',
        'name': 'Sample distribution',
    }

    def test_list(self):
        self.do_test_list()

    def test_reload(self):
        self.do_test_reload()

    def test_create(self):
        self.do_test_create()

    def test_get(self):
        self.do_test_get()


class TestDistribution(V2TestCase):
    pass
