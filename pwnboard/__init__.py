#!/usr/bin/env python3
'''
Initialize all the data and the config info
'''
from flask import Flask
import os
import redis
import json
import logging
from os.path import isfile

BOARD = []


def loadBoard():
    global BOARD
    fil = os.environ.get("BOARD", "board.json")
    with open(fil) as fil:
        BOARD = json.load(fil)

# Create the Flask app
app = Flask(__name__)
app.config['STATIC_FOLDER'] = "lib/static"
logger = logging.getLogger('pwnboard')
loadBoard()
#logfil = getConfig("server/logfile", "")
logfil = ""
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
rserver = os.environ.get('REDIS_HOST', 'localhost')
rport = os.environ.get('REDIS_PORT', 6379)
r = redis.StrictRedis(host=rserver, port=rport,
                      charset='utf-8', decode_responses=True)

# Ignore a few errors here as routes arn't "used" and "not at top of file"
from . import routes  # noqa: E402, F401
