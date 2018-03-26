#!/usr/bin/env python3
import logging
from lib import app
from lib import CONFIG

if __name__ == '__main__':
    logfil = CONFIG.get("logfile", "")
    # Get the pwnboard logger
    log = logging.getLogger("pwnboard")
    # Create a log formatter
    FMT = logging.Formatter(fmt="[%(asctime)s] %(message)s", datefmt="%I:%M:%S")
    # Create a file handler
    if logfil != "":
        FH = logging.FileHandler(logfil)
        FH.setFormatter(FMT)
        log.addHandler(FH)
    # Create a console logging handler
    SH = logging.StreamHandler()
    SH.setFormatter(FMT)
    log.addHandler(SH)
    log.setLevel(logging.DEBUG)
    # Turn off logging for the flask app
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=CONFIG['pwnboard_port'])
