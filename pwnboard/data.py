#!/usr/bin/env python3
import datetime
import time
import os
from . import getConfig, r, logger, genBaseHosts
from functions import send_alert


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
    teams = getConfig("teams", ())
    baseHosts = getConfig("base_hosts", ())
    # If there is no base hosts, regen
    if not baseHosts:
        genBaseHosts()
        baseHosts = getConfig("base_hosts", ())
    # Loop through each host for each team and get the data
    # Turn this data into JSON for the Jinja template
    board = []
    for baseHost in baseHosts:
        data = {}
        data['name'] = baseHost.get("name", "UNKNOWN")
        data['hosts'] = []
        for team in teams:
            # Generate the ip and get the host data for the ip
            ip = baseHost['ip'].replace("x", str(team))
            # Add the host to the list of hosts
            data['hosts'] += [getHostData(ip)]
        board += [data]
    return board


def getHostData(victim):
    '''
    Get the host data for a single host.
    Returns and array with the following information:
    last_seen - The last known callback time
    type - The last service the host called back through
    '''
    # Request the data from the database
    server, app, last, message, online = r.hmget(victim, ('server', 'application',
                                      'last_seen', 'message', 'online'))
    # Add the data to a dictionary
    status = {}
    status['victim'] = victim
    # If all the data is None from the DB, just return the blank status
    # stop unneeded calcs. and prevent data from being written to db
    if all([x is None for x in (server, app, last, message, online)]):
        return status

    # Set the last seen time based on time calculations
    last = getTimeDelta(last)
    if last is None or last > os.environ.get("HOST_TIMEOUT", 2):
        if online.lower().strip() == "true":
            logger.warn("{} offline".format(victim))
            # Try to send a slack message
            send_alert("{} went offline".format(victim))
        status['online'] = False
    else:
        status['online'] = True
    # Write the status to the database
    r.hmset(victim, {'online': status['online']})
    
    status['Last Seen'] = last
    status['App'] = app
    status['Message'] = message
    status['Server'] = server
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
    if time < int(os.environ('ALERT_TIMEOUT', 2)):
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
