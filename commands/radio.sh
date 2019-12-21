#!/bin/bash

if [ $1 == 'on' ]
then
	python3 commands/radio.py on
elif [ $1 == 'off' ]
then
	python3 commands/radio.py off
fi
