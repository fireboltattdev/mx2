class APIError(Exception):
    def __init__(self, response):
        json = response.json()
        self.response = response
        self.errors = json['errors']
        super(APIError, self).__init__(json['message'])

    def __getattr__(self, name):
        try:
            return self.errors[name]
        except KeyError as e:
            raise AttributeError('{0}'.format(e))
