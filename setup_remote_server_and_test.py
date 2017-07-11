#!/bin/bash

ARG1=$1
ARG2=${2:-15139}

# You should 'heroku login' first!
git remote remove heroku
export HEROKU_APP_NAME=$ARG1
heroku create $HEROKU_APP_NAME
git push heroku master

pkill -f "node local.js -s"
node local.js -s $ARG1.herokuapp.com -l $ARG2 > /tmp/$ARG1 &
