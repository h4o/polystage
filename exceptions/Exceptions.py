class CouldNotLog(Exception):
    pass


class BadRequest(Exception):
    pass


class BadCredentials(Exception):
    def __init__(self, tag):
        super(BadCredentials, self).__init__('Missing: {}'.format(tag))


class HTTPError(Exception):
    def __init__(self, message, reason, response):
        super(HTTPError, self).__init__(message, reason)
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code

