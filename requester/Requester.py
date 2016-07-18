import os

import requests

from exceptions import Exceptions
from schema import yaml_loader


class Requester:
    api = {
        'jira': 'rest/api/2/',
        'stash': 'rest/api/1.0/',
        'applinks': 'rest/applinks/1.0/',
        'crowd': 'rest/usermanagement/1/'
    }

    def __init__(self, cred_file='requester/credentials.yml'):
        self.s = requests.Session()
        cred = yaml_loader.load(cred_file, 'schema/credential_schema.yml')
        self.roots = cred['roots']
        self.roots['applinks'] = self.roots['jira']
        self.crowd_auth = (cred['crowd']['app'], cred['crowd']['pwd'])
        self.jira_auth = (cred['credentials']['username'], cred['credentials']['password'])

    def get(self, platform, request, **kwargs):
        return self._request('get', platform, request, **kwargs)

    def post(self, platform, request, **kwargs):
        return self._request('post', platform, request, **kwargs)

    def put(self, platform, request, **kwargs):
        return self._request('put', platform, request, **kwargs)

    def delete(self, platform, request, **kwargs):
        return self._request('delete', platform, request, **kwargs)

    def _request(self, method, platform, request, **kwargs):
        errors = {} if 'errors' not in kwargs else kwargs['errors']

        request = self._get_request(platform, request)
        json, params, auth = kwargs.get('json'), kwargs.get('params'), self._get_auth(platform)

        data, resp = None, None

        if method == 'get':
            resp, data = self._get_rec(request, 0, params=params, auth=auth, headers={'Accept': 'application/json'})
        elif method == 'post':
            resp = self.s.post(request, json=json, params=params, auth=auth, headers={'Accept': 'application/json'})
        elif method == 'put':
            resp = self.s.put(request, json=json, params=params, auth=auth, headers={'Accept': 'application/json'})
        elif method == 'delete':
            resp = self.s.delete(request, json=json, params=params, auth=auth, headers={'Accept': 'application/json'})

        try:
            data = data or resp.json()
        except ValueError as e:
            pass

        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            if resp.status_code in errors.get('reasons', {}):
                raise Exceptions.RequestException(errors.get('message', 'Failure'),
                                                  errors.get('reasons', {}).get(resp.status_code, 'unknown'),
                                                  resp)
            else:
                raise Exceptions.RequestException('Failure', e, resp)
        return data

    def _get_rec(self, request, start, params=None, json=None, auth=None, headers=None):
        params = {} if params is None else params
        params = {**params, **{'start': start}}

        response = self.s.get(request, params=params, json=json, auth=auth, verify=False,
                              headers=headers)
        if response.status_code == 200:
            data = response.json()
            is_last_page = True
            if not isinstance(data, list):
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
        return self.crowd_auth if platform == 'crowd' else self.jira_auth


req = Requester('requester/cred_server.yml')
# req = Requester()