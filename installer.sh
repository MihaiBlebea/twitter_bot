#!/bin/bash

REPO_URL="https://github.com/MihaiBlebea/twitter_bot.git"
FOLDER_NAME="./twitter_bot"

CRON_FILE=/etc/cron.d/twitter_bot_cron
COMMAND="*/2 * * * * ${HOME}/publish.sh > /dev/null 2>&1"

# install or uninstall. that is the question
echo "install or uninstall. that is the question..."
if [[ $* == *-u* ]]; then
	echo "uninstall it is then. sorry to see you leave"
	rm -rf $FOLDER_NAME && \
	rm -rf $CRON_FILE
	echo "finished the uninstall and clean up"
else
	echo "install it is then. continue with it"
	# cloning the repo or just pulling for an update
	if [ -d $FOLDER_NAME ]; then
		echo "folder exists. continue with update..."
		cd $FOLDER_NAME && \
		git pull $REPO_URL
	else
		echo "folder does not exist. just install..."
		git clone $REPO_URL $FOLDER_NAME && \
		cd $FOLDER_NAME
	fi

	# installing the cron tab
	if test -f "$CRON_FILE"; then
		echo "cron file already installed. finishing..."
		exit
	else
		echo "cron file is not here. installing it"
		echo "${COMMAND}" > $CRON_FILE
	fi
	echo "finish the install or update process. all up to date"
fi