from shutil import rmtree

from usr_scripts import *
import inspect
import os
from cmd import Cmd

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from python.scripts.ExcelScript import ExcelScript
from python.scripts.Script import atlas_scripts
from python.util import parse, sort_groupby

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

scripts = []


def generate_help(cmd, func, excel=False):
    doc = inspect.getdoc(func)
    doc = doc if isinstance(doc, str) else ''
    sig = inspect.signature(func)
    arg_list = []
    for name, default in sig.parameters.items():
        arg = name
        if isinstance(default.default, str):
            arg = ''.join([name, '="{}"'.format(default.default)])

        arg_list.append(arg)
    if excel:
        arg_list.append('output_file')

    args = ' '.join(arg_list)
    help_msg = '{doc}\n' \
               '    {cmd} {args}'.format(doc=doc, cmd=cmd, args=args)

    return help_msg


def add_excel(script):
    nb_args_required = len(inspect.signature(script).parameters) + 1

    def generate(self, arg):
        try:
            args = parse(arg, nb_args_required)

            o = script(*args[:-1])
            o.generate(*args[-1:])
        except Exception as e:
            print(e)

    setattr(Shell, 'do_{}'.format(script.__name__), generate)

    help_msg = generate_help(script.__name__, script, excel=True)
    if script.__doc__:
        setattr(Shell, 'help_{}'.format(script.__name__), lambda self, h=help_msg: print(h))


def add_cmd(cmd, func, help_msg=None):
    nb_args_required = len(inspect.signature(func).parameters)

    def temp(self, arg):
        try:
            args = parse(arg, nb_args_required)
            script = func(*args)
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

    def do_test(self, arg):
        repo_path = 'tmp_repo'
        from git import Repo
        url = 'https://pol-lecour:mdp@atlas.i3s.unice.fr/stash/scm/islbd/private.git'
        repo = Repo.clone_from(url, repo_path)
        logs = repo.git.log('--numstat', '--no-merges').splitlines()

        blocs_lines = [index for index, line in enumerate(logs) if line.startswith('commit')]
        blocs = [logs[blocs_lines[i]:blocs_lines[i + 1] - 1] for i in range(0, len(blocs_lines) - 1)]

        deltas_bulk = []
        for bloc in blocs:
            bloc_str = '\n'.join(bloc)

            commit_id = bloc[0].rpartition(' ')[-1]
            author = bloc[1].partition(': ')[-1].rpartition(' ')[0]
            lines = bloc_str.rpartition('\n\n')[-1]
            commit_delta = 0
            for line in lines.splitlines():
                stats = line.split('\t')
                adds = stats[0]
                dels = stats[1]

                if adds == '-' or dels == '-':
                    continue
                commit_delta += int(adds) - int(dels)
            deltas_bulk.append([author, commit_delta])

        deltas = sort_groupby(deltas_bulk, key=lambda d: d[0])
        for author, delta in deltas:
            print(author, '=>', len(list(delta)))
        rmtree(repo_path)

def init_shell():
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
