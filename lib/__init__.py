#!/usr/bin/env python3
'''
Initialize all the data and the config info
'''
from flask import Flask
import redis
import json
import yaml
import logging


def loadConfig():
    global CONFIG
    TOPO_FILE = 'topology.json'
    CONFIG_FILE = 'config.yml'
    # Load a configuration file for the topology
    with open(TOPO_FILE) as of:
        CONFIG.update(json.load(of))
    with open(CONFIG_FILE) as of:
        CONFIG.update(yaml.load(of))

    # Generate a base host list based on the infrustructure configuration
    hostsBase = []
    for network in CONFIG['networks']:
        netip = network.get("ip", "")
        for host in network.get("hosts", ()):
            hostsBase += [{'ip': netip+"."+host.get("ip", "0"),
                           'name': host.get('name', '')}]
    # Add the base host list to the config for later use
    CONFIG['base_hosts'] = hostsBase



# Create the Flask app
app = Flask(__name__)
app.config['STATIC_FOLDER'] = "lib/static"
# Create the topology dict
CONFIG = {}
loadConfig()
# Create the redis object. Make sure that we decode our responses
r = redis.StrictRedis(host=CONFIG['database']['server'],
                      port=CONFIG['database']['port'],
                      charset='utf-8', decode_responses=True)

logger = logging.getLogger('pwnboard')

# Ignore a few errors here as routes arn't "used" and "not at top of file"
from . import routes  # noqa: E402, F401
