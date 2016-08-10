import os
import requests
from os.path import dirname, basename, isfile
import glob
from python.atlas import *
from usr_scripts import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print('\n\nHello there :)')
print("\nType atlas() or excel() to see what's available\n")


def data():
    print(', '.join(os.listdir('data')))


def atlas():
    mods = [file[:-3] for file in os.listdir('usr_scripts/atlas') if
            file.endswith('.py') and not file.startswith('_')]
    print(', '.join(mods))


def excel():
    mods = [file[:-3] for file in os.listdir('usr_scripts/excel') if
            file.endswith('.py') and not file.startswith('_')]
    print(', '.join(mods))
