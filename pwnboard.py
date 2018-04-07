#!/usr/bin/env python3
import logging
from lib import app, getConfig

if __name__ == '__main__':
    # Turn off logging for the flask app
    #log = logging.getLogger("werkzeug")
    #log.setLevel(logging.ERROR)
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=getConfig('server/port', 80))
