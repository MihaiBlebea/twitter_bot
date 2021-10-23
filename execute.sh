#!/bin/bash

if [ "$1" == "publish" ]; then 
	echo "publishing..."
	eval "${PWD}/virtualenv/bin/python3 ${PWD}/src/publish.py \"${@:2}\""
	echo "done"

elif [ "$1" == "schedule" ]; then
	echo "scheduling..."
	eval "${PWD}/virtualenv/bin/python3 ${PWD}/src/content.py \"${@:2}\""
	echo "done"

elif [ "$1" == "report" ]; then
	echo "sending report..."
	eval "${PWD}/virtualenv/bin/python3 ${PWD}/src/daily_report.py \"${@:2}\""
	echo "done"

elif [ "$1" == "followers" ]; then
	echo "sending report..."
	eval "${PWD}/virtualenv/bin/python3 ${PWD}/src/followers.py \"${@:2}\""
	echo "done"

else
	echo "could not find command: $1"
fi
