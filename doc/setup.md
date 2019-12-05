# Pwnboard Setup

# Board Setup
The pwnboard requires a topology to run specifying what IP addresses are in the competition.
The topology is a generic format used by all the different tools for consistency. If the competition does not exist yet, you may generate one or modify an existing one using [Topology-Generator](https://github.com/RITRedteam/Topology-Generator).


Once you have a YAML file with the base topology, a "board" file needs to be generated for the pwnboard. The board file allows for modification of a single IP address and is much more of a verbose configuration file than the generic topology file. The script to convert a topo file into a board file can be downloaded [here](https://github.com/micahjmartin/pwnboard/blob/master/scripts/gen_config.py)

```
curl https://raw.githubusercontent.com/micahjmartin/pwnboard/master/scripts/gen_config.py > gen_config.py
```

Now convert the topology file using the following command
```
python3 gen_config.py topology.json board.json
```

Now when the docker image is built, it will have the correct configuration.

## Deploying

Docker makes deployment of the pwnboard very very simple. See [docker-compose.yml](../docker-compose.yml) for a well-commented example of a docker-compose file with basic configuration options.

You can deploy pwnboard with the following command:
```bash
docker-compose up -d
```

## Notes about the pwnboard

Make sure that `SYSLOG_HOST` is receiving connections or PWNBOARD will lag
when trying to send SYSLOGS. If no syslog server is running, leave it blank.

Further configurations can be made to modify the behavior, the configurations can be set with[Environment Variables](./config.md). 
