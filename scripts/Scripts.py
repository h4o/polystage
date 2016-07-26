from exceptions import Exceptions
from util import eprint


class ReversibleRunner:
    """Allow to create a reversible script.
    Any command run with a instance of this class is stored and ready to be undone if a problem occurs

    If never_undo is set to True, the future command executed with the method do will never be undone by the runner \
    unless the method parameter never_undo is set to False"""

    def __init__(self):
        self.never_undo = False
        self.history = []

    def do(self, command, never_undo=None):
        """never_undo can take 3 values
        * True: the runner will never try to undo this command
        * False: the runner will try to undo this command if an error occurs even if the class attribute never_undo is \
        set to True => the method parameter never_undo has priority over the class attribute never_undo"""

        if never_undo is None:
            never_undo = self.never_undo
        try:
            result = command.do()
            if not never_undo:
                self.history.insert(0, command)
            return result
        except Exceptions.RequestException as e:
            eprint('Failure:', e, '\nTrying to undo:')
            self.revert()
            # TODO: Create a more explicit exception
            raise Exception("Script failure")

    def revert(self):
        for command in self.history:
            command.undo(safe=True)


class NeverUndo:
    def __init__(self, runner):
        self.script = runner

    def __enter__(self):
        self.script.never_undo = True
        return self.script

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.script.never_undo = False
