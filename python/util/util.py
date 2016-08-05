import pprint
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def pp(elem):
    p = pprint.PrettyPrinter(depth=6)
    p.pprint(elem)
