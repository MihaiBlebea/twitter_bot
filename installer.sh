#!/bin/bash

REPO_URL="https://github.com/MihaiBlebea/twitter_bot.git"
FOLDER_NAME="twitter_bot"

CRON_FILE=/etc/cron.d/twitter_bot_cron
COMMAND="*/2 * * * * ${HOME}/${FOLDER_NAME}/publish.sh >> ${HOME}/twitter_bot_logs.log 2>&1"

# check dependencies
checkfor () {
	command -v $1 >/dev/null 2>&1 || {
		echo >&2 "$1 required"
		exit 1
	}
}

# run the function to check for git dependency
checkfor "git"

# check the install status
if [[ $* == *-c* ]]; then
	echo "check the status of the install:"

	# check the repo folder
	if [ -d "./$FOLDER_NAME" ]; then
		echo -e "\xE2\x9C\x94 repo folder exists"
	else
		echo -e "x repo folder missing"
	fi

	# check if virtual env created
	if [ -d "./$FOLDER_NAME/virtualenv" ] || [ -d "./virtualenv" ]; then
		echo -e "\xE2\x9C\x94 virtual env exists"
	else
		echo -e "x virtual env missing"
	fi

	# check if the crontab file exists
	if test -f "$CRON_FILE"; then
		echo -e "\xE2\x9C\x94 crontab file exists"
	else
		echo -e "x crontab file missing"
	fi

	exit 0
fi

# install or uninstall. that is the question
echo "install or uninstall. that is the question..."
if [[ $* == *-u* ]]; then
	echo "uninstall it is then. sorry to see you leave"
	rm -rf "./$FOLDER_NAME" && \
	rm -rf $CRON_FILE
	echo "finished the uninstall and clean up"
else
	echo "install it is then. continue with it"
	# cloning the repo or just pulling for an update
	if [ -d "./$FOLDER_NAME" ]; then
		echo "folder exists. continue with update..."
		cd "./$FOLDER_NAME" && \
		git pull $REPO_URL
	else
		echo "folder does not exist. just install..."
		git clone $REPO_URL "./$FOLDER_NAME" && \
		cd "./$FOLDER_NAME"
	fi

	# check if virtualenv has been activated
	if [ -d "./$FOLDER_NAME/virtualenv" ] || [ -d "./virtualenv" ]; then
		echo "virtualenv already created"
	else
		echo "virtualenv not created yet. starting now"
		if [ ${PWD##*/} == $FOLDER_NAME ]; then
			python3 -m venv virtualenv && pip3 install -r requirements.txt
		else
			cd "./$FOLDER_NAME" && \
			python3 -m venv virtualenv && \
			pip3 install -r requirements.txt
		fi
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