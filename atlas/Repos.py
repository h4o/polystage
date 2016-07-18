from exceptions import Exceptions
from requester.Requester import req
from util import eprint


def create(project_key, name, scm_id='git', forkable=True):
    errors = {
        'message': 'Could not create the repository {}'.format(name),
        'reasons': {
            409: 'The repository already exists'
        }
    }
    json = {
        'name': name,
        'scmId': scm_id,
        'forkable': forkable
    }
    try:
        req.post('stash', 'projects/{}/repos'.format(project_key), json=json, errors=errors)
        print('The repository {} has been created'.format(name))
    except Exceptions.RequestException as e:
        eprint(e)
