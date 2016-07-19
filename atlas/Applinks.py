from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


@rest_request
def link(jira_key, bitbucket_key):
    app_id = get_application_id()
    json = {'applicationId': app_id, 'typeId': 'stash.project', 'key': bitbucket_key}

    req.put('applinks', 'entitylink/jira.project/{}'.format(jira_key), json=json)
    print('Projects linked')


@rest_request
def get_application_id():
    app_list = req.get('applinks', 'listApplicationlinks')['list']
    for app in app_list:
        if app['application']['displayUrl'] == (req.roots['stash'].strip('/')):
            return app['application']['id']
