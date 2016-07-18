from requester.Requester import req

from exceptions import Exceptions
from util import eprint


def link(jira_key, bitbucket_key):
    app_id = get_application_id()
    json = {'applicationId': app_id, 'typeId': 'stash.project', 'key': bitbucket_key}
    try:
        req.put('applinks', 'entitylink/jira.project/{}'.format(jira_key), json=json)
        print('Projects linked')
    except Exceptions.RequestException as e:
        eprint(e)


def get_application_id():
    try:
        app_list = req.get('applinks', 'listApplicationlinks')['list']
        for app in app_list:
            if app['application']['displayUrl'] == (req.roots['stash'].strip('/')):
                return app['application']['id']
    except Exceptions.RequestException as e:
        eprint(e)
