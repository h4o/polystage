from python.atlas.Command import NotUndoable

from python.requester.Requester import Requester


class Link(NotUndoable):
    def __init__(self, jira_key, bitbucket_key):
        self.jira_key = jira_key
        self.bitbucket_key = bitbucket_key

    def _do(self):
        app_id = GetApplicationId().do()
        json = {'applicationId': app_id, 'typeId': 'stash.project', 'key': self.bitbucket_key}

        Requester.req.put('applinks', 'entitylink/jira.project/{}'.format(self.jira_key), json=json)
        print('Projects linked')


class GetApplicationId(NotUndoable):
    def _do(self):
        app_list = Requester.req.get('applinks', 'listApplicationlinks')['list']
        for app in app_list:
            if app['application']['displayUrl'] == (Requester.req.roots['stash'].strip('/')):
                return app['application']['id']
