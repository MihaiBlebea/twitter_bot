#!/bin/bash

echo "starting the deploy process..."

# run the tests
./virtualenv/bin/python3 -m unittest discover -s test -p "*_test.py"

if [[ "$?" != 0 ]]; then
	echo "could not deploy. tests are not passing"
	exit 1
fi

ssh silverpi "curl https://raw.githubusercontent.com/MihaiBlebea/twitter_bot/master/installer.sh --output installer.sh --silent && chmod +x ./installer.sh && ./installer.sh"

echo "finished!"