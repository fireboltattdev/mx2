from m2x.resource import Collection, Item


class Key(Item):
    PATH = 'keys/{key}'

    def regenerate(self):
        return self.post(self.path('regenerate'))


class Keys(Collection):
    PATH = 'keys'
    ITEMS_KEY = 'keys'
    ITEM_CLASS = Key


class FeedKeys(Keys):
    PATH = Keys.PATH + '?feed={feed_id}'
