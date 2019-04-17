#!/usr/bin/env python3
import random
import requests
import json
import time
import sys

hosts = ["10.x.1.10",  "10.x.1.20", "10.x.1.30", "10.x.1.40", "10.x.1.50",
         "10.x.2.2", "10.x.2.3", "10.3.x.3"]
server = "http://localhost/generic"

try:
    loop = int(sys.argv[1])
except Exception as E:
    loop = 30
while True:
    ip = random.choice(hosts).replace("x", str(random.randint(1, 10)))
    data = json.dumps({'ip': ip, "application": "empire"})
    headers = {'Content-Type': 'application/json', 'Connection': 'Close'}
    try:
        r = requests.post(server, headers=headers, data=data,
                          verify=False)
        r = r.text
    except Exception as E:
        r = "Invalid"
    print("{}: {}".format(data, r))
    time.sleep(loop)
