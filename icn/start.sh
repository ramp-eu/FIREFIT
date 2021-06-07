#!/bin/bash

# turn on bash's job control
set -m

# start the primary process and put it in the background
#
#### Switch flowers_model.zip with your own model ###
#
python ./icn.py -f flowers_model.zip &

# strart the api process
gunicorn --config python:icn_api.server_config api:app

# pring the primary process back into the foreground and leave it there
fg %1

