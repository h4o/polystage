import inspect
import os
from cmd import Cmd

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from python.scripts.ExcelScript import ExcelScript
from python.scripts.Script import atlas_scripts
from python.util import parse
from usr_scripts import *
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

scripts = []


def generate_help(cmd, func):
    doc = inspect.getdoc(func)
    doc = doc if isinstance(doc, str) else ''
    sig = inspect.signature(func)
    arg_list = []
    for name, default in sig.parameters.items():
        arg = name
        if isinstance(default.default, str):
            arg = ''.join([name, '="{}"'.format(default.default)])

        arg_list.append(arg)
        if isinstance(func, ExcelScript):
            arg_list.append('output_file')

    args = ' '.join(arg_list)
    help_msg = '{doc}\n' \
               '    {cmd} {args}'.format(doc=doc, cmd=cmd, args=args)

    return help_msg


def add_excel(script):
    def generate(self, arg):
        try:
            args = parse(arg)
            # TODO Instead of -1 check the number of args, so the error when an argument is missing is more accurate
            o = script(*args[:-1])
            o.generate(*args[-1:])
        except Exception as e:
            print(e)

    setattr(Shell, 'do_{}'.format(script.__name__), generate)

    help_msg = generate_help(script.__name__, script)
    if script.__doc__:
        setattr(Shell, 'help_{}'.format(script.__name__), lambda self, h=help_msg: print(h))


def add_cmd(cmd, func, help_msg=None):
    def temp(self, arg):
        try:
            script = func(*parse(arg))
            scripts.append(script)
        except Exception as e:
            print(e)

    setattr(Shell, 'do_{}'.format(cmd), temp)
    if func.__doc__:
        module = func.__module__.split('.')[-1]
        setattr(Shell, 'help_{}'.format(module), lambda self, h=func.__doc__: print(h))

    help_msg = generate_help(cmd, func)
    if help_msg:
        setattr(Shell, 'help_{}'.format(cmd), lambda self, h=help_msg: print(h))


class Shell(Cmd):
    prompt = ':'

    def do_EOF(self, arg):
        """ctrl + d : exit the shell"""
        return True

    def do_undo(self, arg):
        """Undo the last script executed"""
        if scripts:
            scripts.pop().revert()
        else:
            print('Nothing to undo')

    def do_data(self, arg):
        """Display files in the data folder"""
        print(', '.join(os.listdir('data')))


def init_shell():
    # TODO add as a doc the parameters expected
    # TODO is some parameters are missing, prompt them
    for f in atlas_scripts:
        m = f.__module__.split('.')[-1]
        add_cmd(m, f)
    subs = ExcelScript.__subclasses__()
    for s in subs:
        add_excel(s)


if __name__ == '__main__':
    init_shell()
    shell = Shell()
    shell.cmdloop()
