import pprint
import sys
import string
import random

__all__ = ['eprint']


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def pp(elem):
    p = pprint.PrettyPrinter(depth=6)
    p.pprint(elem)


def pw_gen(size=8, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))


def parse(arg):
    return tuple(arg.split())