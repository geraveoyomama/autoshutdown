#!/bin/bash

INTERFACE="enp5s0" #$(ip -o -4 route show to default | awk '{print $5}')
OVERRIDE_SPEED=100 #KB/s
SAMPLES=1200
MIN_SPEED=4 #KB/s
echo $INTERFACE

function worker () {
  local network=()
  while true; do
    SPEED=$(printf %.0f "$(ifstat -i "$INTERFACE" 1 1 | awk '{print $1+$2}' | sed -n '3p')")
    if [[ "$SPEED" -ge "$OVERRIDE_SPEED" ]] ; then
    local network=()
    else
      if [[ ((${#network[@]} -ge $SAMPLES)) ]] ; then
        network=("${network[@]:1}")
      fi
      network+=("$SPEED")
      SUM_SPEED=$(IFS=+; echo "$((${network[*]}))")
      LEN_NETWORK=${#network[@]}
      AVG_SPEED=$((SUM_SPEED / LEN_NETWORK))
      if [[ ! $(who) ]] && ([[ "$AVG_SPEED" -le "$MIN_SPEED" ]] && [[ "$LEN_NETWORK" -ge "$SAMPLES" ]]); then
        /sbin/shutdown -h +0
      fi
    fi
done
}

worker
