#!/bin/bash

ARG1=$1 # app name
ARG2=${2:-15139} # listen port
ARG3=$3 # password

# You should 'heroku login' first!
git remote remove heroku
export HEROKU_APP_NAME=$ARG1
heroku create $HEROKU_APP_NAME
git push heroku master
heroku config:set KEY=$3

pkill -f "node local.js -s"
node local.js -s $ARG1.herokuapp.com -l $ARG2 > /tmp/$ARG1 &
