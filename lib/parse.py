#!/usr/bin/env python3
from . import r
from . import logger


def processEvent(event):
    '''
    Process events pass into the slack channel
    '''
    if 'empire' in event['text']:
        parse_empire(event)
    elif 'cobaltstrike' in event['text']:
        parse_cobaltstrike(event)
    else:
        parse_linux(event)


def parseData(data):
    '''
    Parse updates that come in via POST to the server
    '''
    if data['ip'] == "127.0.0.1":
        return
    logger.debug("updated beacon for {} from {}".format(data['ip'], data['type']))
    status = Status(**data)
    status.save()


def parse_linux(event):
    # "%s %s backdoor active on %s"
    text = event['text']
    status = Status()
    status.ip = text.split(' ')[5]
    status.host = text.split(' ')[0]
    status.session = text.split(' ')[1]
    status.last_seen = event['ts']
    status.save()


def parse_empire(event):
    text = event['text']
    status = Status(type='empire')
    if "new agent" in text:
        # kali new agent on 10.0.2.15; agent: HLT4VKEK;
        # platform: Linux,kali,4.7.0-kali1-amd64,#1 SMP Debian 4.7.5-1kali3
        # (2016-09-29),x86_64; type: empire
        status.ip = text.split(' ')[4].replace(';', '')
        status.host = text.split(' ')[0]
        status.session = text.split(' ')[6].replace(';', '')
        status.last_seen = event['ts']
        status.save()
    else:
        # kali empire agent EHUDM1C7 checked in
        session = text.split(' ')[3]
        status = Status(session=session, type='empire')
        status.ip = r.get(status.session)
        status.host, s, t, status.last_seen = r.hmget(status.ip,
                                                      ('host', 'session',
                                                       'type', 'last_seen'))
        status.last_seen = event['ts']
        status.save()


def parse_cobaltstrike(event):
    text = event['text']
    print(text)
    status = Status(type='cobaltstrike')
    if "new beacon" in text:
        # teamserver new beacon on 192.168.1.160; beacon id: 94945;
        # platform: Windows; type: cobaltstrike
        status.ip = text.split(' ')[4].replace(';', '')
        status.host = text.split(' ')[0]
        status.session = text.split(' ')[7].replace(';', '')
        status.last_seen = event['ts']
        print(status)
        status.save()

    else:
        # cobaltstrike beacon 94945 checked in
        session = text.split(' ')[2]
        status = Status(session=session, type='cobaltstrike')
        status.ip = r.get(status.session)
        status.host, s, t, status.last_seen = r.hmget(status.ip,
                                                      ('host', 'session',
                                                       'type', 'last_seen'))
        status.last_seen = event['ts']
        print(status)
        status.save()


class Status(object):
    def __init__(self, ip=None, host=None, session=None, type=None,
                 last_seen=None):
        self.ip = ip
        self.host = host
        self.session = session
        self.type = type
        self.last_seen = last_seen

    def __str__(self,):
        return "ip: %s, host: %s, session: %s, type: %s, last_seen: %s" % (
            self.ip, self.host, self.session, self.type, self.last_seen)

    def save(self,):
        r.hmset(self.ip, {'host': self.host, 'session': self.session,
                          'type': self.type, 'last_seen': self.last_seen})
        if self.type == 'empire':
            r.set(self.session, self.ip)
