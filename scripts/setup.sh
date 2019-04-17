#!/bin/bash

# If there is a toplogy file, but not a board file, generate the baord
# from the topology.json
TOPO="config/topology.json"
BOARD="board.json"
if [ -f "$TOPO" ] && [ ! -f "$BOARD" ]; then
    echo "Generating $BOARD from $TOPO"
    python3 "scripts/gen_config.py" "$TOPO" "$BOARD"
fi
