class CouldNotLog(Exception):
    pass


class BadRequest(Exception):
    pass


class BadCredentials(Exception):
    def __init__(self, tag):
        super(BadCredentials, self).__init__('Missing: {}'.format(tag))


class RequestException(Exception):
    def __init__(self, message, reason, response):
        super(RequestException, self).__init__(message, reason)
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code


class ScriptFailure(Exception):
    def __init__(self, initial_exception):
        super(ScriptFailure, self).__init__('Script Failure', initial_exception)
        self._initial_exception = initial_exception

    @property
    def initial_exception(self):
        return self._initial_exception
