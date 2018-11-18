from utils import logs
import json

def get():
    """Returns a dict with msgcount pairs from the logfile.
    Creates the file if it doesn't exist"""
    try:
        with open(logs.get_logname(), 'r') as file:
            return {int(k):v for (k,v) in json.load(file).items()}
    except FileNotFoundError:
        dump({})
        return {}

def dump(msgcount):
    """dumps message count to a json file"""
    with open(logs.get_logname(), 'w+') as file:
        logfile = json.dump(msgcount, file)
