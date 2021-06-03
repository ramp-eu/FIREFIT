#!/bin/bash

# turn on bash's job control
set -m

# start the primary process and put it in the background
python ./icn.py &

# save model to DB
python icn_lib/add_model.py flowers_model.zip

# strart the api process
gunicorn --config python:icn_api.server_config api:app

# pring the primary process back into the foreground and leave it there
fg %1

