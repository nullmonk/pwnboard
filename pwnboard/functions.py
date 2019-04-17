#!/usr/bin/env python3
from . import r
from . import logger


def saveData(data):
    '''
    Parse updates that come in via POST to the server.

    'ip' and 'application' are required in the data
    '''
    print("data  has been saved")
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
