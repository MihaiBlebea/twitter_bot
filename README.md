# Twitter bot for posting an update and retweeting


## How to install?
You need to have `ansible` installed locally.
Run this command:
```bash
make ansible-deploy
```


## How to run?
#### To post an update use this command:
```bash
twitter_bot -m="update message" -u="https://mihablebea.com" -f
```
-m flag message to post in the update
-u flag url to attach to the update
-f flag for ignoring the fact that the update was already posted

#### To retweet a random tweet based on query tag use this command:
```bash
twitter_bot q="golang" -f
```
-q flag for adding a query tag for searching a tweet
-f flag for ignoring the fact that the update was already posted


## How to uninstall?
You need to have `ansible` installed locally.
Run this command:
```bash
make ansible-remove
```