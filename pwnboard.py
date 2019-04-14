#!/usr/bin/env python3

import os
from pwnboard import app

if __name__ == '__main__':
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 80))
    debug = os.environ.get("FLASK_DEBUG", "false")
    debug = debug.lower().strip() in ["true", "yes", "1", "t"]
    app.run(host=host, debug=debug, port=port)
