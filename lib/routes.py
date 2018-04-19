#!/usr/bin/env python3
import json
import logging
from .data import getBoardDict, getEpoch, getAlert
from . import getConfig, app, logger, r, loadConfig, writeConfig, dumpConfig
from .parse import processEvent, parseData
from flask import (request, render_template, make_response, Response, url_for,
                   redirect, abort)
from .tools import sendSlackMsg

# The cache of the main board page
BOARDCACHE = ""
BOARDCACHE_TIME = 0
BOARDCACHE_UPDATED = True


@app.route('/', methods=['GET'])
def index():
    '''
    Return the board with the most recent data (cached for 10 seconds)
    '''
    html = ""
    log = logging.getLogger('werkzeug')

    # Find the time since the last cache
    # The server will return the cache in two situations
    #  1. It has been less than 'cache_time' since the last cache
    #  2. There has been no new data since the last cache AND the cache is
    #     younger than 30 seconds
    cache = getConfig('server/cache', True)
    if cache:
        global BOARDCACHE
        global BOARDCACHE_TIME
        global BOARDCACHE_UPDATED
        ctime = getEpoch() - BOARDCACHE_TIME
        if (ctime < getConfig('server/cache_time', 10) or
                (not BOARDCACHE_UPDATED and ctime < 30)):
            log.info("Pulling board html from cache")
            # return the cached dictionary
            return make_response(BOARDCACHE)
    # Get the board data and render the template
    error = getAlert()
    board = getBoardDict()
    alttheme = getConfig('alternate_theme', False)
    html = render_template('index.html', error=error, alttheme=alttheme,
                           board=board, teams=getConfig('teams', ()))
    # Update the cache and the cache time
    if cache:
        BOARDCACHE_TIME = getEpoch()
        BOARDCACHE = html
        BOARDCACHE_UPDATED = False
    return make_response(html)


@app.route('/slack-events', methods=['POST'])
def slack_events():
    res = request.json
    if res.get('challenge', None):
        return request.json['challenge']

    # to get the 'channel' value right click on the channel and copy link
    # I.E C9PGYTYH5
    if res.get('event', None) and res.get('event')['channel'] == '':
        processEvent(res['event'])

    # Tell us that new data has come
    global BOARDCACHE_UPDATED
    BOARDCACHE_UPDATED = True
    return ""


@app.route('/generic', methods=['POST'])
def genericEvent():
    req = request.get_json(force=True)
    if req.get('challenge', None):
        return req.json['challenge']
    data = {}

    # Type and IP are required
    if 'type' in req:
        data['type'] = req.get('type')
    else:
        return "Invalid data"

    # Host and Session are not required
    data['host'] = None
    data['session'] = None
    # Time is calculated
    data['last_seen'] = getEpoch()
    # If its one IP, update that, if its more than one, add them all
    if 'ip' in req:
        try:
            data['ip'] = req.get('ip').split('/')[0]
            parseData(data)
        except Exception as Exp:
            pass
    elif 'ips' in req and isinstance(req.get('ips'), list):
        print("Got several IP addresses", req.get('ips'))
        for addr in req.get('ips'):
            try:
                data['ip'] = addr.split('/')[0]
                parseData(data)
            except Exception as Exp:
                pass
    else:
        return "Invalid data"
    # Tell us that new data has come
    global BOARDCACHE_UPDATED
    BOARDCACHE_UPDATED = True
    return "Valid"


@app.route('/install/<tool>/', methods=['GET'])
@app.route('/install/<tool>', methods=['GET'])
def installTools(tool):
    '''
    Returns a script that can be used as an installer for the specific tool.
    E.g. If you request '/install/empire' you will get a script to run that
    will update your empire with the needed functions
    '''
    host = getConfig('server/host', 'localhost:80')
    # Try to render a template for the tool
    try:
        text = render_template('clients/{}.j2'.format(tool), server=host)
        logger.info("{} requested {} install script".format(
                                                request.remote_addr, tool))
        return Response(text+"\n", mimetype='text/plain')
    except Exception as E:
        print(E)
        abort(404)


@app.route('/setmessage', methods=['GET', 'POST'])
def setmessage():
    '''
    Updates the message alert at the top of the page
    '''
    # If it is a get, return a text box to set the message
    if request.method == 'GET':
        return Response(render_template('setmessage.html',
                                        alerttime=getConfig('alert_timeout',
                                                            1)+1))
    msg = request.form.get('message', "")
    if msg == "":
        return "Invalid: 'message' must contain text"
    user = request.form.get('user', "")
    if user == "":
        user = request.remote_addr
    sendSlackMsg('{} says "{}"'.format(user, msg))
    logger.info('{} updated message to "{}"'.format(user, msg))
    # The data stored in redis
    data = {}
    # Update the time the message was set
    data['time'] = getEpoch()
    data['message'] = msg
    # Store the message in the redis db
    r.hmset('alert', data)
    # If the message was pushed via the browser, redirect it home
    if request.form.get('browser', "0") == "1":
        return redirect(url_for('index'))
    # if its an API call then return valid
    return "Valid"


@app.route('/reload', methods=['GET'])
def reload():
    loadConfig()
    return redirect(url_for('index'))


@app.route('/dumpconfig', methods=['GET'])
def dumpRoute():
    return Response(dumpConfig(), mimetype='application/json')


@app.route('/uploadconfig', methods=['POST'])
def uploadRoute():
    req = request.get_json(force=True)
    writeConfig(req)
    return "Valid"
