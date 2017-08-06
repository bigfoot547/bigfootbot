#!/bin/bash

last_exit=0

echo "+----------------------------+" >> bot.log
echo "| SEPARATOR                  |" >> bot.log
echo "+----------------------------+" >> bot.log
echo "$(date +"%b %d %Y %R:%S"): bot.sh executed." >> bot.log

while [ $last_exit -ne 2 ]; do
	echo "$(date +"%b %d %Y %R:%S"): Bot starting..." >> bot.log
	python3 main.py
	last_exit=$(( $? ))
	echo "$(date +"%b %d %Y %R:%S"): The bot has exited with code ${last_exit}." >> bot.log
done

echo "$(date +"%b %d %Y %R:%S"): Ctrl+C pressed, bot aborting." >> bot.log
