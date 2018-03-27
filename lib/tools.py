from . import getConfig, logger
import requests
import json


def sendSlackMsg(msg, force=False):
    '''
    Send a slack message to the appropriate channel
    '''
    if not getConfig('slack/send_updates', False) and not force:
        return True
    # Get the token and channel from the config file
    token = getConfig("slack/token")
    channel = getConfig("slack/channel", "#pwnboard")
    if not token:
        logger.warn("configuration missing slack token")
        return False
    if not channel:
        logger.warn("configuration missing slack channel")
        return False
    if msg == "":
        logger.warn("Slack message should not be blank")
        return False

    # Prepare the request data
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer '+token}
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
