from uuid import uuid4

from python.atlas.Command import NotUndoable, Command
from python.requester.Requester import Requester


class BoardType:
    KANBAN = 'kanban'
    SCRUM = 'scrum'


class GetAll(NotUndoable):
    def _do(self):
        boards = Requester.req.get('agile', 'board')['values']
        return boards


class Create(Command):
    def __init__(self, type, project_name, name=None):
        self.name = name or project_name
        self.type = type
        self.project_name = project_name
        self.id = None

    def _do(self):
        new_filter = CreateFilter(self.project_name).do()
        board = Requester.req.post('agile', 'board', json={
            'name': self.name,
            'type': self.type,
            'filterId': new_filter['id']
        })
        self.id = board['id']
        print('The {} board {} for the project {} has been created'.format(self.type, self.name, self.project_name))
        return board

    def _undo(self):
        Delete(self.id).do()


class Delete(NotUndoable):
    def __init__(self, board_id):
        self.board_id = board_id

    def _do(self):
        Requester.req.delete('agile', 'board/{}'.format(self.board_id))

        print('The board {} has been deleted'.format(self.board_id))


class CreateFilter(NotUndoable):
    def __init__(self, project_name):
        self.project_name = project_name

    def _do(self):
        new_filter = Requester.req.post('jira', 'filter', json={
            'name': str(uuid4()),
            'jql': 'project="{}"'.format(self.project_name)
        })

        print('The filter has been created')
        return new_filter
