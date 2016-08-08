import requests
from python.atlas import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from python.scripts.Script import public, registry

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print('Hello there :)')
print('Type \'help\' to know the commands available')


def helpme():
    print('NOTHING YET !')
    print('A little, though : ', registry)
