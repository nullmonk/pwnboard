#!/usr/bin/env python3
'''
Initialize all the data and the config info
'''
from flask import Flask
import redis
import json

# Create the redis object. Make sure that we decode our responses
r = redis.StrictRedis(host='localhost', charset="utf-8", decode_responses=True)
# Create the Flask app
app = Flask(__name__, static_url_path='/static')
app.debug = True
# Create the Config dict
CONFIG = {}
CONFIG_FILE = 'config.json'
# Load a configuration file for the data
with open(CONFIG_FILE) as of:
    CONFIG = json.load(of)
# Generate a base host list based on the infrustructure configuration
hostsBase = []
for network in CONFIG['networks']:
    netip = network.get("ip", "")
    for host in network.get("hosts", ()):
        hostsBase += [{'ip': netip+"."+host.get("ip", "0"),
                       'name': host.get('name', '')}]
# Add the base host list to the config for later use
CONFIG['base_hosts'] = hostsBase

# Ignore a few errors here as routes arn't "used" and "not at top of file"
from . import routes  # noqa: E402, F401
