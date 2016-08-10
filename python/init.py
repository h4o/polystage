import requests
from python.atlas import *
from usr_scripts import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print('Hello there :)')
print('Type helpme() to know the commands available')


def helpme():
    print('NOTHING YET !')
