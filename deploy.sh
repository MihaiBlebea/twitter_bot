#!/bin/bash

echo "starting the deploy process..."

ssh silverpi "curl https://raw.githubusercontent.com/MihaiBlebea/twitter_bot/master/installer.sh --output installer.sh --silent && chmod +x ./installer.sh && ./installer.sh"

echo "finished!"