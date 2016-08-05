from atlas import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requester.Requester import Requester
from util.util import pp

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def debug():
    pp(Requester.req.roots)


print("Hello there :)")
