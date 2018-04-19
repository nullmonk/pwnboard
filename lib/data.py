#!/usr/bin/env python3
import datetime
import time
from . import getConfig, r, logger, genBaseHosts
from .tools import sendSlackMsg


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


def getHostData(host):
    '''
    Get the host data for a single host.
    Returns and array with the following information:
    last_seen - The last known callback time
    type - The last service the host called back through
    '''
    # Request the data from the database
    h, s, t, last, o = r.hmget(host, ('host', 'session',
                                      'type', 'last_seen', 'online'))
    # Add the data to a dictionary
    status = {}
    status['ip'] = host
    # If all the data is None from the DB, just return the blank status
    # stop unneeded calcs. and prevent data from being written to db
    if (t is None and last is None and o is None
        and h is None and s is None):
        return status
    # Set the last seen time based on time calculations
    last = getTimeDelta(last)
    if last is None or last > getConfig('host_timeout', 2):
        if o == "True":
            logger.warn("{} offline".format(host))
            # Try to send a slack message
            sendSlackMsg("<!channel> {} went offline :eyes:".format(host))
        status['online'] = False
    else:
        status['online'] = True
    # Write the status to the database
    r.hmset(host, {'online': status['online']})
    # Add only the values that are not None
    # redisdata=[('Host', h), ('Session', s), ('Type', t), ('Last seen', last)]
    # We dont actually need session and host
    redisdata = [('Type', t), ('Last seen', last)]
    for item in redisdata:
        if item[1] is not None:
            status[item[0]] = item[1]
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
    if time < getConfig('alert_timeout', 1):
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
