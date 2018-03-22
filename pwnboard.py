#!/usr/bin/env python3
from lib import app
from lib import CONFIG

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG['pwnboard_port'])
