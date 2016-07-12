import yaml

import Roles
from Requester import req
from exceptions import Exceptions
from schema import yaml_loader
from util import eprint


def import_projects(file, create_roles=False):
    p = yaml_loader.load('schema/project_sample.yml', 'schema/project_schema.yml')

    for project in p['projects']:
        print("Trying to delete : " + project['key'])
        delete(project['key'])

    for project in p['projects']:
        lead = project.get('lead', project['developers'][0])
        create(project['key'], project['name'], lead)
    #
    # project = p['projects'][0]
    # lead = project.get('lead', project['developers'][0])
    # # delete(project['key'])
    # create(project['key'], project['name'], lead)


def _import_project(project, create_roles=False):
    params = project['parameters']
    members = project['members']
    roles = members.keys()

    create(params['key'], params['name'], params['lead'], params.get('description', ''))

    for role_name in roles:
        role = Roles.get(role_name)
        if role is None and create_roles:
            role = Roles.create(role_name)
        for member in members[role_name]:
            add_to_role(params['key'], member, role.get('id', None))


def add_to_role(project_key, user, role_id):
    errors = {
        'message': 'Could not add user {} to the project {} for the role {}'.format(user, project_key, role_id),
        'reasons': {
            404: 'Either the group, the role or the project does not exist or the user is already in it'
        }
    }
    try:
        req.post('jira', 'project/{}/role/{}'.format(project_key, role_id), json={'user': [user]}, errors=errors)
        print('The user {} has been added to the project {} for the role {}'.format(user, project_key, role_id))
    except Exceptions.RequestException as e:
        eprint(e)


def create(key, name, lead, description=''):
    project = {
        'key': key,
        'name': name,
        'projectTypeKey': 'business',
        'description': description,
        'lead': lead
    }
    errors = {
        'message': 'Could not create project {}'.format(name),
        'reasons': {
            400: 'Invalid request. Leader unknown or the project already exists'
        }
    }
    try:
        response = req.post('jira', 'project', json=project, errors=errors)
        print('The project {} has been created'.format(name))
        return response
    except Exceptions.RequestException as e:
        eprint(e)


def delete(key):
    errors = {
        'message': 'Could not delete project {}'.format(key),
        'reasons': {
            403: 'You do not have the permissions to delete the project',
            404: 'The project does not exist'
        }
    }
    try:
        req.delete('jira', 'project/{}'.format(key), errors=errors)
        print('The project {} has been deleted'.format(key))
    except Exceptions.RequestException as e:
        eprint(e)


if __name__ == '__main__':
    import_projects('projects.yml', True)