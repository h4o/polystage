from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


@rest_request
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

    req.post('stash', 'projects/{}/repos'.format(project_key), json=json, errors=errors)
    print('The repository {} has been created'.format(name))


@rest_request
def delete(project_key, repo_name):
    message = 'Could not delete the repo {} from the project {}'.format(repo_name, project_key)
    reason = 'The repo does not exist'
    repo = get(project_key, repo_name) or {}
    repo_slug = repo.get('slug')
    if not repo_slug:
        raise Exceptions.RequestException(message, reason, None)
    req.delete('stash', 'projects/{}/repos/{}'.format(project_key, repo_slug))
    print('The repository {} from the project {} has been deleted'.format(repo_name, project_key))


@rest_request
def delete_all(project_key):
    repos = get_all(project_key)

    for repo in repos:
        delete(project_key, repo['name'])


@rest_request
def get(project_key, repo_name):
    repos = get_all(project_key)
    match = None
    for repo in repos:
        if repo['name'].upper() == repo_name.upper():
            match = repo
            break
    return match


@rest_request
def get_all(project_key):
    return req.get('stash', 'projects/{}/repos'.format(project_key))['values']
