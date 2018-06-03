# PWNboard
PWNboard for RIT redteam engagements and competitions

Modified version of ztgrace/pwnboard

# Running the PWNboard
## Install
#### Flask
Install all the needed packages and the pwnboard code
```
apt-get install -y redis-server python3-redis python3-flask python3-yaml
git clone https://github.com/micahjmartin/pwnboard /var/www/pwnboard
chown -R www-data:www-data /var/www/pwnboard
```

#### nginx and uwsgi
If you plan on running pwnboard behind nginx, run the following commands in
addition to the previous.

Install Packages
```
apt-get install nginx uwsgi uwsgi-plugins-python3
```

Set up the systemd service file and the nginx config
```
ln -s /var/www/pwnboard/serv/pwnboard.service /lib/systemd/system/
systemctl daemon-reload
ln -s /var/www/pwnboard/serv/nginx.conf /etc/nginx/sites-enabled/pwnboard.conf
# Delete the default nginx page
rm /etc/nginx/sites-enabled/default
```

Generate Self-Signed SSL certificates
```
mkdir /etc/nginx/ssl
openssl req -x509 -nodes -new -batch -keyout /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.crt
```

> If you would like to use LetsEncrypt's Certbot, follow
[this guide](CERTBOT.md).

## Configure

__Mandatory Configurations:__ Make sure to update the url with the domain name
if you are using the framework integrations
```yaml
server:
  host: https://pwnboard.local
```

### Topology
Configure the topology json file by running `./scripts/generate_topo.py` or by
hand modifying the sample config `topology.json`.


### Settings
All non-topology settings can be updated in `config.yml`.

You may configure how long (in minutes) a host has before it times out
```yaml
host_timeout: 5
```

**Slack**

Setup slack information in the `config.yml` file.
Pwnboard can push slack updates everytime a host times out.
Enable the settings in the configuration file to allow this functionality.
```yaml
slack:
  token: "xoxb-123456789123-xxXXxXXXxXXXXxxxxXxXXXXxxXX"
  channel: "#pwnboard"
  send_updates: true
```

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
Generic installation scripts can be used to push updates via bash and Python for
other integrations as well.

### Currently supported frameworks:
**CobaltStrike** `http://localhost/install/cobaltstrike`

**Metasploit** `http://localhost/install/metaspoit`

**Empire** `http://localhost/install/empire`

**Python** `http://localhost/install/python`

**Bash** `http://localhost/install/bash`

> Make sure `  host:` is updated in the configuration so the install
scripts render correctly


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

## Running
#### Flask
To directly run the Flask app, run `python3 /var/www/pwnboard.py`
from the commandline

#### uWSGI/NGINX
Make sure you follow the installation instructions for nginx/uwsgi and then
run `systemctl start pwnboard`



# Future Features
* Init script to help configure and use the program
* Reset the db before starting an engagement
* Click on a host to track the beacons


![pwnboard](https://raw.githubusercontent.com/micahjmartin/pwnboard/master/doc/img/PWNboard.png)
