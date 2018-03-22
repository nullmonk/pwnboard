#!/usr/bin/env python3
import datetime
import time
from . import CONFIG, r


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
    teams = CONFIG.get("teams", ())
    baseHosts = CONFIG.get("base_hosts", ())
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


def getHostData(host):
    '''
    Get the host data for a single host.
    Returns and array with the following information:
    last_seen - The last known callback time
    type - The last service the host called back through
    '''
    # Request the data from the database
    h, s, t, last = r.hmget(host, ('host', 'session',
                                   'type', 'last_seen'))
    # Add the data to a dictionary
    status = {}
    status['ip'] = host
    # Set the last seen time based on time calculations
    last = getTimeDelta(last)
    # Add only the values that are not None
    redisdata = [('Host', h), ('Session', s), ('Type', t), ('Last seen', last)]
    for item in redisdata:
        if item[1] is not None:
            status[item[0]] = item[1]
    return status


def getTimeDelta(ts):
    try:
        checkin = datetime.datetime.fromtimestamp(float(ts))
        diff = datetime.datetime.now() - checkin
        minutes = int(diff.total_seconds()/60)
        return minutes
    except Exception as E:
        return None
