# pwnboard
The pwnboard is a tool used for RIT redteam engagements and competitions. It allows Redteam to
easily see which machines they have access to and which machines they have lost beacons on.

This is a modified version of ztgrace/pwnboard.

## Running the pwnboard

For RIT Redteam engagements, the pwnboard is deployed with [RedTeamDeploy](https://github.com/micahjmartin/RedTeamDeploy). For custom deployments, see [Pwnboard Setup](./doc/setup.md).


## Watching the pwnboard

To watch all of your lovely beacons flowing in, simply navigate to the pwnboard in a webbrowser.

## Updating the pwnboard
If you would like your C2s and tools to update the pwnboard, you may use some of the plugins provided. Currently, the following public C2s are supported:
  - CobaltStrike - `http://PWNBOARD/install/cobaltstrike`
  - Empire - `http://PWNBOARD/install/empire`
  - Metasploit - `http://PWNBOARD/install/metasploit`

If you would like to get another C2 framework supported, please make an issue or you can start integrating directly. Code examples for updating the pwnboard are provided in the following languages:
  - Bash - `http://PWNBOARD/install/bash`
  - Python - `http://PWNBOARD/install/python`
  - Golang - `http://PWNBOARD/install/go`


> Make sure `PWNBOARD_URL` is updated in the environment so the install scripts render correctly


## Set Alert Message
Too push an alert message to the page you can navigate to `/setmessage` or push
and update with a post request
```
curl -X POST 127.0.0.1/setmessage -d 'message=PWNboard'
```

> Note this feature may be broken...

# Future Features
* Click on a host to track the beacons

![pwnboard](https://raw.githubusercontent.com/micahjmartin/pwnboard/master/doc/img/PWNboard.png)
