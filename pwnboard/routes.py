#!/usr/bin/env python3
import json
import logging
from flask import (request, render_template, make_response, Response, url_for,
                   redirect, abort, jsonify)


from .data import getBoardDict, getEpoch, getAlert
from . import getConfig, app, logger, r, loadConfig, writeConfig, dumpConfig
from .parse import saveData

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


@app.route('/callback', methods=['POST'])
def callback():
    """Handle when a server registers an callback"""
    data = request.get_json(force=True)
    if 'challenge' in data:
        return data['challenge']
    data['last_seen'] = getEpoch()
    # Make sure 'application' is in the data
    if 'application' not in data: return "invalid POST"

    if 'victims' in data and isinstance(data['victims'], list):
        for victim in data['victims']:
            d = dict(data)
            d['victim'] = victim
            saveData(d)
    elif 'victim' in data:
        saveData(data)
    else:
        return 'invalid POST'
    # Tell us that new data has come
    global BOARDCACHE_UPDATED
    BOARDCACHE_UPDATED = True
    return "valid"
    


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
