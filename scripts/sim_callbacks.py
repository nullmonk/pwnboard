#!/usr/bin/env python3
import random
import requests
import json
import time
import sys

hosts = ["10.2.x.1",  "10.2.x.2", "10.2.x.3", "10.2.x.4", "10.2.x.5",
         "10.3.x.1", "10.3.x.2", "10.3.x.3"]
server = "https://pwnboard.win/generic"

try:
    loop = int(sys.argv[1])
except Exception as E:
    loop = 30
while True:
    ip = random.choice(hosts).replace("x", str(random.randint(1, 10)))
    data = json.dumps({'ip': ip, "type": "empire"})
    headers = {'Content-Type': 'application/json', 'Connection': 'Close'}
    try:
        r = requests.post(server, headers=headers, data=data,
                          verify=False)
        r = r.text
    except Exception as E:
        r = "Invalid"
    print("{}: {}".format(data, r))
    time.sleep(loop)
