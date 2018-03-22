#!/usr/bin/env python3

from .data import getBoardDict
from . import CONFIG, app
from .parse import processEvent
from flask import request, render_template, make_response


@app.route('/', methods=['GET'])
def index():
    error = ""
    board = getBoardDict()
    resp = make_response(render_template('index.html', error=error,
                         board=board, teams=CONFIG['teams']))
    return resp


@app.route('/slack-events', methods=['POST'])
def slack_events():
    res = request.json
    if res.get('challenge', None):
        return request.json['challenge']

    # to get the 'channel' value right click on the channel and copy link
    # I.E C9PGYTYH5
    if res.get('event', None) and res.get('event')['channel'] == '':
        processEvent(res['event'])

    return ""
