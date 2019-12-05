# Configuration Settings

Each setting can be set as an environment variable in docker-compose.yml. Below is all the
environment variables and their default settings.


- `PWNBOARD_URL` _No default_ - Used to set the url for the code in `/install/<tool>`. Usually looks something like this `http://pwn.board.com:8080` or `http://pwnboard.hack`

- `BOARD` _Default: "./board.json"_ - The location of the board configuration file. This really has no use case

- `PWN_THEME` _Default: "blue"_ - The theme of the pwnboard, `blue` is Red for active hosts and Blue for dead hosts. `green` is Green for active hosts and Red for dead hosts.

- `REDIS_HOST` _Default: "localhost"_ - The location of the redis server
- `REDIS_PORT` _Default: "6379"_ - The location of the redis server


- `FLASK_HOST` _Default: "0.0.0.0"_ - Which interface Flask should bind to
- `FLASK_PORT` _Default: "80"_ - Which port Flask should bind to
- `FLASK_DEBUG` _Default: "false"_ - Whether or not flask should be in debug mode

- `CACHE_TIME` _Default: "-1"_ - How many seconds to cache the web page for. Default is do not cache at all. This may be needed if you have many people watching the board at once.

- `HOST_TIMEOUT` _Default: 2_ - Number of minutes of inactivity before a host expires

- `ALERT_TIMEOUT` _Default: 2_ - Number of minutes to show an alert for. _Note: This feature might actually be broken..._


- `SYSLOG_HOST` _No default_ - If HOST and PORT are set for SYSLOG, send syslog data to the server on every callback
- `SYSLOG_PORT` _No default_
