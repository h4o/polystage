from python.atlas.Command import NotUndoable, Command
from python.requester.Requester import Requester


class GetAll(NotUndoable):
    def _do(self):
        boards = Requester.req.get('agile', 'board')['values']
        return boards


class Create(Command):
    def __init__(self, type, name, project):
        self.type = type
        self.name = name
        self.project = project

    def _do(self):
        errors = {
            'message': 'The {} board {} for the project {} could not be created'.format(self.type, self.name,
                                                                                        self.project),
            'reasons': {
                400: ''
            }
        }

        print('The {} board {} for the project {} has been created'.format(self.type, self.name, self.project))

    def _undo(self):
        pass
