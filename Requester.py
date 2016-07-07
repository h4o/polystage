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
        request = self._get_request(platform, request)
        return self._get_rec(request, 0, self._get_auth(platform), **kwargs)

    def post(self, platform, request, **kwargs):
        auth = self._get_auth(platform)
        request = self._get_request(platform, request)
        result = self.s.post(request, json=kwargs.get('json'), params=kwargs.get('params'), auth=auth)

        result.raise_for_status()
        return result

    def delete(self, platform, request, **kwargs):
        auth = self._get_auth(platform)
        request = self._get_request(platform, request)
        result = self.s.delete(request, params=kwargs.get('params'), auth=auth)

        result.raise_for_status()
        return result

    def _get_rec(self, url, start, auth=None, **kwargs):
        params = {
            'start': start
        }
        params = {**kwargs.get('params', {}), **params}
        r = self.s.get(url, params=params, json=kwargs.get('json'), auth=auth, headers={'Accept': 'application/json'})
        if r.status_code == 200:
            res = r.json()
            if 'isLastPage' in res and not res['isLastPage']:
                next_res = self._get_rec(url, res['nextPageStart'])
                res['values'] += next_res['values']
                res['size'] += next_res['size']
            return res
        else:
            raise Exceptions.BadRequest

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
