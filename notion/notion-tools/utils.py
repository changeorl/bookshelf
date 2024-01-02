import requests
from settings import *
import json
import os

def api_debug(response, cli=1, output=0, log=0, finish=0):
    print(f"{response.request.method}@{response.url} finished!")
    if cli:
        print(f"printed @below.")
        print(json.dumps(response.json(), indent=4))
    if output:
        fname = os.path.join(PATH.output, "output.json")
        entries={
            "request": response.request.method,
            "url": response.url,
            "response": response.json()
        }
        save2json(entries, fname)
        print(f"exported @{fname}")
    if log:
        fname = os.path.join(PATH.output_today, f"{TIME.now}.json")
        entries={
            "request": response.request.method,
            "url": response.url,
            "response": response.json()
        }
        save2json(entries, fname)
        print(f"archived @{fname}")
    if finish:
        exit()
    
def debug_print(x):
    print(f"printed @below.")
    print(json.dumps(x, indent=4))

def debugfile(response):
    fname = f"{PATH.output}/output.json"
    save2json(response, fname)
    print(f"exported @{fname}")

def log(response):
    suffix = response.json()['object']
    fname = f"{PATH.output_today}/{TIME.now}_{suffix}.json"
    save2json(response, fname)
    print(f"archived @{fname}")

def save2json(data, fname=None):
    with open(fname, 'w') as f:
        json.dump(data, f, indent=4)
