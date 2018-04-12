#!/usr/bin/env python3

from lib import app

if __name__ == '__main__':
    from lib import getConfig
    app.run(host='0.0.0.0', port=getConfig('server/port', 80))
