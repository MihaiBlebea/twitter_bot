# Python script maker for linux


## How to install?
Run this command:
```bash
curl https://raw.githubusercontent.com/MihaiBlebea/twitter_bot/master/installer.sh --output installer.sh --silent && chmod +x ./installer.sh && ./installer.sh
```


## How to run?
Run this command:
```bash
chmod +x ${HOME}/twitter_bot/publish.sh && ${HOME}/twitter_bot/publish.sh
```

Or if the permission to execute has already been assigned, then run:
```bash
${HOME}/twitter_bot/publish.sh
```


## How to uninstall?
Option 1 - with the installer file: 
```bash
./installer.sh -u
```

Option 2 - download the installer and uninstall in one command:
```bash
curl https://raw.githubusercontent.com/MihaiBlebea/twitter_bot/master/installer.sh --output installer.sh --silent && chmod +x ./installer.sh && ./installer.sh -u && rm -rf ./installer.sh
```