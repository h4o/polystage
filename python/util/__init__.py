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


def to_ascii(number, digit, base=26):
    str_repr = []
    while True:
        mod = number % base
        str_repr.insert(0, chr(mod + ord('A')))
        number = (number - mod) // base
        if number <= 0:
            break

    return ''.join(str_repr).rjust(digit, 'A')
