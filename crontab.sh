#!/bin/bash

# if there is no position argument just return help
if [ "$#" -eq 0 ]; then
    echo "help - run as: $0 <command> -u?"
	exit 1
fi

COMMAND=$1

# define the functions
setcrontab () {
	( crontab -u $USER -l; echo "$COMMAND" ) | crontab -u $USER -
}


removecrontab () {
    crontab -u $USER -l | grep -v "$COMMAND" | crontab -u $USER -
}


checkcrontab () {
	CHECK=$(crontab -u $USER -l | grep "$COMMAND")
}


# just a simple check
if [[ $* == *-c* ]]; then
	echo "checking if the crontab is installed, returns 0 for true, 1 for false"
	checkcrontab

	if [[ $CHECK == *"$COMMAND"* ]]; then
		exit 0
	else
		exit 1
	fi
fi


# check if the crontab is already set
checkcrontab

echo $CHECK
echo $COMMAND

# do the logic in here
if [[ $CHECK == *"$COMMAND"* ]]; then
	echo "< $COMMAND > cron command is already set"
	if [[ $* == *-u* ]]; then
		echo "removing cron command < $COMMAND >"
		removecrontab
	fi
else 
	echo "< $COMMAND > cron command is not set"
	if [[ $* != *-u* ]]; then
		echo "installing cron command < $COMMAND >"
		setcrontab
	fi
fi