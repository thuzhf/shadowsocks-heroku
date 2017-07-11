#!/bin/bash

node local.js -s $1.herokuapp.com -l $2 > /tmp/$1 &
