class CouldNotLog(Exception):
    pass


class BadRequest(Exception):
    pass


class BadCredentials(Exception):
    def __init__(self, tag):
        super(BadCredentials, self).__init__('Missing: {}'.format(tag))

