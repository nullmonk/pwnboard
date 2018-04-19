#!/usr/bin/env python3
'''
Initialize all the data and the config info
'''
from flask import Flask
import redis
import json
import yaml
import logging
from os.path import isfile

# Create the topology dict
CONFIG = {}


def getConfig(key, default=None):
    '''
    Get a value from the config. If it is not there, use the default
    and log it
    '''
    retval = CONFIG
    for i in key.split("/"):
        if i in retval:
            retval = retval[i]
        else:
            logger.warn("Missing config value {}, using {}".format(key,
                                                                   default))
            return default
    return retval


def dumpConfig():
    '''
    Dump the config file
    '''
    global CONFIG
    # Remove all the base hosts information from the config
    basehosts = CONFIG.pop("base_hosts",None)
    data = json.dumps(CONFIG, indent=2) + "\n"
    genBaseHosts()
    return data

def writeConfig(config = None):
    '''
    overwrite the in-memory config file
    '''
    global CONFIG
    # If we are given a new config, update the global to that
    if config:
        CONFIG = config
    # Write the config file
    with open(CONFIG.get('MAIN_CONF', 'tmp.json'), 'w') as conf:
        conf.write(json.dumps(CONFIG, indent=2))
    genBaseHosts()


def loadConfig():
    global CONFIG
    TOPO_FILE = 'topology.json'
    CONFIG_FILE = 'config.yml'
    if not isfile(TOPO_FILE):
        TOPO_FILE = "/etc/pwnboard/" + TOPO_FILE
    if not isfile(CONFIG_FILE):
        CONFIG_FILE = "/etc/pwnboard/" + CONFIG_FILE
    # Load a configuration file for the topology
    with open(TOPO_FILE) as of:
        CONFIG.update(json.load(of))
    with open(CONFIG_FILE) as of:
        CONFIG.update(yaml.load(of))
    CONFIG['MAIN_CONF'] = "tmp.json"
    writeConfig()


def genBaseHosts():
    # Generate a base host list based on the infrustructure configuration
    global CONFIG
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
logger = logging.getLogger('pwnboard')
loadConfig()
logfil = getConfig("server/logfile", "")
# Get the pwnboard logger
# Create a log formatter
FMT = logging.Formatter(fmt="[%(asctime)s] %(levelname)s: %(message)s",
                        datefmt="%x %I:%M:%S")
# Create a file handler
if logfil != "":
    FH = logging.FileHandler(logfil)
    FH.setFormatter(FMT)
    logger.addHandler(FH)
# Create a console logging handler
SH = logging.StreamHandler()
SH.setFormatter(FMT)
logger.addHandler(SH)
logger.setLevel(logging.DEBUG)
# Create the redis object. Make sure that we decode our responses
rserver = getConfig('database/server', 'localhost')
rport = getConfig('database/port', 6379)
r = redis.StrictRedis(host=rserver, port=rport,
                      charset='utf-8', decode_responses=True)

# Ignore a few errors here as routes arn't "used" and "not at top of file"
from . import routes  # noqa: E402, F401
