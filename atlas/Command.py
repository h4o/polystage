from abc import abstractmethod, ABC

from exceptions import Exceptions
from util import eprint


class Command(ABC):
    def do(self, safe=False):
        try:
            return self._do()
        except Exceptions.RequestException as e:
            if safe:
                eprint(e)
            else:
                raise e

    def undo(self, safe=True):
        try:
            return self._undo()
        except Exceptions.RequestException as e:
            if safe:
                eprint(e)
            else:
                raise e

    @abstractmethod
    def _do(self):
        pass

    @abstractmethod
    def _undo(self):
        pass


class NotUndoable(Command):
    def _undo(self):
        print(self, "Cannot be undone")
