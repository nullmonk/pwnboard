#!/usr/bin/env python3
import datetime
import time
import os
import copy
from . import r, logger, BOARD
from .functions import send_alert


def getEpoch():
    '''
    Return the current Epoch time
    '''
    return time.mktime(datetime.datetime.now().timetuple())


def getBoardDict():
    '''
    Generate a game board based on the config file
    Get all the DB info for each host
    '''
    # Get the teams and the basehost list from the config
    board = copy.deepcopy(BOARD['board'])
    for row in board:
        for _host in row['hosts']:
            _host.update(getHostData(_host['ip']))
    return board


def getHostData(ip):
    '''
    Get the host data for a single host.
    Returns and array with the following information:
    last_seen - The last known callback time
    type - The last service the host called back through
    '''
    # Request the data from the database
    server, app, last, message, online = r.hmget(ip, ('server', 'application',
                                      'last_seen', 'message', 'online'))
    # Add the data to a dictionary
    status = {}
    status['ip'] = ip
    # If all the data is None from the DB, just return the blank status
    # stop unneeded calcs. and prevent data from being written to db
    if all([x is None for x in (server, app, last, message, online)]):
        return status

    # Set the last seen time based on time calculations
    last = getTimeDelta(last)
    if last > int(os.environ.get("HOST_TIMEOUT", 2)):
        if online and online.lower().strip() == "true":
            logger.warn("{} offline".format(ip))
            # Try to send a slack message
            send_alert("{} went offline".format(ip))
        status['online'] = ""
    else:
        status['online'] = "True"
    # Write the status to the database
    r.hmset(ip, {'online': status['online']})

    status['Last Seen'] = "{}m".format(last)
    status['Type'] = app
    return status


def getAlert():
    '''
    Pull the alert message from redis if is is recent.
    Return nothing if it is not recent
    '''
    time, msg = r.hmget("alert", ('time', 'message'))
    time = getTimeDelta(time)
    if time is None or msg is None:
        return ""
    # If the time is within X minutes, display the message
    if time < int(os.environ.get('ALERT_TIMEOUT', 2)):
        return msg
    return ""


def getTimeDelta(ts):
    '''
    Print the number of minutes between now and the last timestamp
    '''
    try:
        checkin = datetime.datetime.fromtimestamp(float(ts))
        diff = datetime.datetime.now() - checkin
        minutes = int(diff.total_seconds()/60)
        return minutes
    except Exception as E:
        return None

def saveData(data):
    '''
    Parse updates that come in via POST to the server.

    'ip' and 'application' are required in the data
    '''
    if data.get('ip', '127.0.0.1').lower() in ["127.0.0.1", "none", None, "null"]:
        return

    logger.debug("updated beacon for {} from {}".format(data['ip'], data['application']))
    # Fill in default values. Fastest way according to https://stackoverflow.com/a/17501506
    data['message'] = data['message'] if 'message' in data else ""
    data['server'] = data['server'] if 'server' in data else ""

    # save this to the DB
    r.hmset(data['ip'], {
        'application': data['application'],
        'message': data['message'],
        'server': data['server'],
        'last_seen': data['last_seen']
    })


def send_alert(message):
    pass
