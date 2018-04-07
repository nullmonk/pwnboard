#!/usr/bin/env python3
import logging
from .data import getBoardDict, getEpoch, getAlert
from . import getConfig, app, logger, r, loadConfig
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
    if 'ip' in req:
        data['ip'] = req.get('ip')
    else:
        return "Invalid data"
    # Host and Session are not required
    data['host'] = None
    data['session'] = None
    # Time is calculated
    data['last_seen'] = getEpoch()
    parseData(data)
    logger.info(
        "{} updated beacon for {} from {}".format(request.remote_addr,
                                                  data['ip'], data['type']))
    # Tell us that new data has come
    global BOARDCACHE_UPDATED
    BOARDCACHE_UPDATED = True
    return "Valid"


@app.route('/arsenal', methods=['POST'])
def arsenalIntegration():
    '''
    Receive and parse data for arsenal webhooks... This isnt the APIs job kyle...
    '''
    req = request.get_json(force=True)
    ip_addrs = []
    try:
        for iface in target.facts.get('interfaces', []):
            addrs = iface.get('ip_addrs')
            if addrs:
                for addr in addrs:
                    if addr != '127.0.0.1' and not addr.startswith('169.254'):
                        ip_addrs.append(addr)
    except:
        return "Invalid"
    return "Ok"


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
        text = Response(render_template('clients/{}.j2'.format(tool),
                                        server=host),
                                        mimetype='text/plain')
        logger.info("{} requested {} install script".format(
                                                request.remote_addr, tool))
        return text + "\n"
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
def relaod():
    loadConfig()
    return redirect(url_for('index'))
