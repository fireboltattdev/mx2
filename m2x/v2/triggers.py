from m2x.v2.resource import Resource


class Trigger(Resource):
    COLLECTION_PATH = 'devices/{device_id}/triggers'
    ITEM_PATH = 'devices/{device_id}/triggers/{id}'
    ITEMS_KEY = 'triggers'

    def __init__(self, api, device, **data):
        self.device = device
        super(Trigger, self).__init__(api, **data)

    def test(self):
        return self.api.post(
            self.item_path(device_id=self.device.id, id=self.id) + '/test'
        )

    @classmethod
    def list(cls, api, device, **params):
        # Search parameters: query, tags, page, limit
        path = cls.collection_path(device_id=device.id)
        return super(cls, cls).list(api, path=path, itemize_options={
            'device': device
        }, **params)

    @classmethod
    def create(cls, api, device, **attrs):
        path = cls.collection_path(device_id=device.id)
        return super(cls, cls).create(api, path=path, itemize_options={
            'device': device
        }, **attrs)

    @classmethod
    def get(cls, api, device, id, **params):
        path = cls.item_path(id, device_id=device.id)
        return super(cls, cls).get(api, id, path=path, itemize_options={
            'device': device
        }, **params)

    @classmethod
    def item_update(cls, api, device, id, **params):
        path = cls.item_path(id, device_id=device.id)
        return super(cls, cls).item_update(api, id, path=path, **params)
