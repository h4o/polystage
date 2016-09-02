import pprint
import sys
import string
import random
from itertools import groupby

__all__ = ['eprint']


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def pp(elem):
    p = pprint.PrettyPrinter(depth=6)
    p.pprint(elem)


def pw_gen(size=8, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))


def parse(arg, check=False):
    args = tuple(arg.split())
    if check:
        if len(args) != check:
            raise Exception('Bad number of arguments, type help for more info')
    return args


def to_ascii(number, digit, base=26):
    str_repr = []
    while True:
        mod = number % base
        str_repr.insert(0, chr(mod + ord('A')))
        number = (number - mod) // base
        if number <= 0:
            break

    return ''.join(str_repr).rjust(digit, 'A')


def sort_groupby(iterable, key):
    return groupby(sorted(iterable, key=key), key=key)
