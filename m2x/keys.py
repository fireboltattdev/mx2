from m2x.resource import Collection, Item


class Key(Item):
    PATH = 'keys/{key}'

    def regenerate(self):
        url = self.api.url(self.path(self.PATH + '/regenerate'))
        response = self.api.request(url=url, method='POST',
                                    allow_redirects=False)
        if response.status_code == 303:
            key = response.headers['location'].rsplit('/', 1)[-1]
            details = self.api.get(self.PATH.format(key=key))
            self.set_data(details)


class Keys(Collection):
    PATH = 'keys'
    ITEMS_KEY = 'keys'
    ITEM_CLASS = Key


class FeedKeys(Keys):
    PATH = Keys.PATH + '?feed={feed_id}'

    def create(self, **attrs):
        return super(FeedKeys, self).create(feed=self.feed_id, **attrs)
