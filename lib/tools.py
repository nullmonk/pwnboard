from . import getConfig, logger
import requests
import json

SLACK_TOKEN = None

def getSlackKey():
    '''
    Read the slack API token from the config
    '''
    global SLACK_TOKEN
    token_file = getConfig("slack/token_file")
    try:
        with open(token_file, 'r') as slkfil:
            SLACK_TOKEN = slkfil.read().strip()
        if SLACK_TOKEN is None or SLACK_TOKEN == "":
            raise Exception("Bad slack token")
        return True
    except Exception as E:
        logger.warn("No slack token file")
        return False


def sendSlackMsg(msg, force=False):
    '''
    Send a slack message to the appropriate channel
    '''
    if not getConfig('slack/send_updates', False) and not force:
        return True

    # Get the slack token
    if SLACK_TOKEN is None:
        if not getSlackKey():
            logger.warn("configuration missing slack token")
            return False
    # Get the token and channel from the config file
    channel = getConfig("slack/channel", "#pwnboard")
    if msg == "":
        logger.warn("Slack message should not be blank")
        return False

    # Prepare the request data
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer '+SLACK_TOKEN}
    data = {'channel': channel, 'text': msg, 'as_user': 'true'}
    host = "https://slack.com/api/chat.postMessage"
    try:
        req = requests.post(host, data=json.dumps(data), headers=headers)
        req = req.json()
        if req['ok']:
            logger.debug("Slack message sent to {}".format(channel))
            return True
        else:
            logger.warn("Slack error: {}".format(json.dumps(req)))
            return False
    except Exception as E:
        logger.error(E)
        return False
