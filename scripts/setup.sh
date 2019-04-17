#!/bin/sh

# If there is a toplogy file, but not a board file, generate the baord
# from the topology.json
TOPO="topology.json"
BOARD="board.json"

# Check topo in the main dir first
if [ -f "$TOPO" ] && [ ! -f "$BOARD" ]; then
    echo "Generating $BOARD from $TOPO"
    python3 "scripts/gen_config.py" "$TOPO" "$BOARD"
    exit
fi


TOPO="config/topology.json"
if [ -f "$TOPO" ] && [ ! -f "$BOARD" ]; then
    echo "Generating $BOARD from $TOPO"
    python3 "scripts/gen_config.py" "$TOPO" "$BOARD"
    exit
fi
