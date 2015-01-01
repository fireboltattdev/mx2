class APIError(Exception):
    def __init__(self, response):
        self.json = response.json()
        self.response = response
        super(APIError, self).__init__(self.json.get('message'))

    @property
    def errors(self):
        return self.json.get('error') or []

    def __getattr__(self, name):
        try:
            return self.errors[name]
        except KeyError as e:
            raise AttributeError('{0}'.format(e))


class InactiveAccountError(APIError):
    @property
    def errors(self):
        return ['Account is inactive']
