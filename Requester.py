import os
import requests
import yaml

from exceptions import Exceptions


class Requester:
    api = {
        'jira': 'rest/api/2/',
        'stash': 'rest/api/1.0/',
        'crowd': 'rest/usermanagement/1/'
    }

    def __init__(self, cred_file='credentials.yml'):
        self.s = requests.Session()
        cred = Credentials(cred_file)
        self.roots = cred['roots']
        self.crowd_auth = (cred['crowd']['app'], cred['crowd']['pwd'])
        data = cred['credentials']

        auth_url = os.path.join(self.roots['jira'], 'rest/auth/1/session/')
        auth_jira = self.s.post(auth_url, json=data, verify=False)

        if auth_jira.status_code != 200:
            raise Exceptions.CouldNotLog()

    def get(self, platform, request, **kwargs):
        return self._request('get', platform, request, **kwargs)

    def post(self, platform, request, **kwargs):
        self._request('post', platform, request, **kwargs)

    def delete(self, platform, request, **kwargs):
        self._request('delete', platform, request, **kwargs)

    def _request(self, method, platform, request, **kwargs):
        errors = {} if 'errors' not in kwargs else kwargs['errors']

        request = self._get_request(platform, request)
        json, params, auth = kwargs.get('json'), kwargs.get('params'), self._get_auth(platform)

        data, response = None, None

        if method == 'get':
            response, data = self._get_rec(request, 0, params=params, auth=auth)
        elif method == 'post':
            response = self.s.post(request, json=json, params=params, auth=auth)
        elif method == 'delete':
            response = self.s.delete(request, json=json, params=params, auth=auth)

        if response.status_code in errors.get('reasons', {}):
            raise Exceptions.HTTPError(errors.get('message', 'Failure'),
                                       errors.get('reasons', {}).get(response.status_code, 'unknown'),
                                       response)
        else:
            response.raise_for_status()

        return data

    def _get_rec(self, request, start, params=None, json=None, auth=None):
        params = {**params, **{'start': start}}

        response = self.s.get(request, params=params, json=json, auth=auth, headers={'Accept': 'application/json'})
        if response.status_code == 200:
            data = response.json()

            is_last_page = data.get('isLastPage', True)
            if not is_last_page:
                next_res, next_data = self._get_rec(request, data['nextPageStart'])
                data['values'] += next_data['values']
                data['size'] += next_data['size']
            return response, data
        else:
            return response, None

    def _get_request(self, platform, url):
        return os.path.join(self.roots[platform], self.api[platform], url)

    def _get_auth(self, platform):
        return self.crowd_auth if platform == 'crowd' else None


class Credentials:
    mandatory_tags = {
        'roots': ['jira', 'stash', 'crowd'],
        'credentials': ['username', 'password'],
        'crowd': ['app', 'pwd'],
    }

    def __init__(self, file='credentials_poly.yaml'):
        with open(file) as f:
            self.cred = yaml.safe_load(f)

            # Checks if credential file structure is respected
            tag = self._missing_tag(self.cred, Credentials.mandatory_tags)
            if tag is not None:
                raise Exceptions.BadCredentials(tag)

            for node in self.cred:
                tag = self._missing_tag(self.cred[node], Credentials.mandatory_tags[node])
                if tag is not None:
                    raise Exceptions.BadCredentials('node: ' + tag)

    def __getitem__(self, index):
        return self.cred[index]

    def _missing_tag(self, dictionary, mandatory_tags):
        for tag in mandatory_tags:
            if tag not in dictionary:
                return tag
        return None


req = Requester()
