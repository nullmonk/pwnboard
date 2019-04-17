""" An example of a plugin. """

import requests
import functools
from lib.common.plugins import Plugin
from lib.common.plugins import Plugin
import lib.common.helpers as helpers

# anything you simply write out (like a script) will run immediately when the
# module is imported (before the class is instantiated)
print("Hello from your new plugin!")

# this class MUST be named Plugin
class Plugin(Plugin):
    description = "A plugin to feed session checkins to the pwnboard and Sawmill"

    def onLoad(self):
        self.mainMenu = None
        self.pwnboard = "http://pwnboard.win/checkin"
        self.sawmill = "logs.pwnboard.win"
        self.sawmillport = 5000
        #dispatcher.connect(self.event_handler, sender=dispatcher.Any)

    def register(self, mainMenu):
        """ any modifications to the mainMenu go here - e.g.
        registering functions to be run by user commands """
        mainMenu.__class__.do_lumberjack = self.do_lumberjack

        self.mainMenu = mainMenu  # Save this object for later

        # Make the agent checkin call our agent checkin first
        mainMenu.agents.update_agent_lastseen_db = self.wrapper(
            mainMenu.agents.update_agent_lastseen_db,
            self.hook_agent_lastseen_db
        )

    def do_lumberjack(self, args):
        """Print the current configuration for lumberjack
        TODO: allow updates to the URLS
        """
        print(helpers.color("[*] Lumberjack plugin has been loaded!"))
        print(helpers.color("[*] \tPwnboard URL: {}".format(self.pwnboard)))
        print(helpers.color("[*] \tSawmill URL: {}:{}".format(self.sawmill, self.sawmillport)))

    def hook_agent_lastseen_db(self, sessionID):
        """Function hook for agents.update_..._db() that will let us know
        when agents check in"""
        session_data = self.mainMenu.agents.get_agent_db(sessionID)  # Get the session info
        victim_ip = session_data['internal_ip'].split()[0]  # Ip of callback
        #update_pwnboard([victim_ip], name="empire")
        print(victim_ip, sessionID)

    def wrapper(self, func, func2):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            func2(*args, **kwargs)
            return func(*args, **kwargs)
        return wrap

    def update_pwnboard(ips, name="python"):
        host = "{{ server }}/generic"
        data = {'ips': ips, 'type': name}
        try:
            req = requests.post(host, json=data, timeout=3)
            print(req.text)
            return True
        except Exception as E:
            print(E)
            return False

