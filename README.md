# PWNboard
PWNboard for RIT redteam engagements and competitions

Modified version of ztgrace/pwnboard

# Running the PWNboard
## Install
```
apt-get install -y redis-server python3-redis python3-flask python3-yaml
git clone https://github.com/micahjmartin/pwnboard
```
## Configure
### Topology
Configure the topology json file by running `./scripts/generate_topo.py` or by
hand modifying the sample config `toplogy.json`.


### Settings
All non-topology settings can be updated in `config.yml`.

**Slack**

Setup slack information in the `config.yml` file and modify the database settings
if you are running the Redis DB somewhere else.

**Alternate Theme**

Some of my fellow red teamers wanted a theme where Red means it is
controlled by redteam and Blue is controlled by blueteam. You may enable this in
the configuration file.
```yaml
alternate_theme: true
```

> Anytime the configuration file is changed, navigate to `/reload` so the 
app will reload the changes

## Setup Frameworks
If you are adding hooks to frameworks such as cobaltstrike or empire,
run the install scripts for each framework and client.
The install scripts will be rendered based off of the current configuration file.

### Currently supported frameworks:
**CobaltStrike** `http://localhost/install/cobaltstrike/` or `/install/cs`

**Empire** `https://localhost/install/empire`

> Make sure `server` and `port` are updated in the configuration so the install
scripts render correctly

## Run
Run `./pwnboard.py` from the commandline

### Set Alert Message
Too push an alert message to the page you can navigate to `/setmessage` or push
and update with a post request
```
curl -X POST 127.0.0.1/setmessage -d 'message=PWNboard'
```

The time (in minutes) that the message will be displayed can be set in the
config file.
```yaml
alerttime: 2
```

# Future Features
* Init script to help configure and use the program
* Reset the db before starting an engagement
* Click on a host to track the beacons REQUIRE DB UPDATE


![pwnboard](https://raw.githubusercontent.com/micahjmartin/pwnboard/master/img/PWNboard.png)
