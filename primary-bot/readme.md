## Use GitPod
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://github.com/mikeysan/retweet_anything/tree/main/primary-bot)

# Primary Bot

This twitter bot is used to retweet posts about topics that I find interesting.
The retweets are based on hashtags; example, #opensource, #eddiehub

It is possible to copy this folder only as it is indpendent from the others; i.e. secret details are stored within this folder

### How to run

- On Linux:

```py
python3 twitterBot.py
```
- On Windows:

```py
python twitterBot.py
```



#### TODO:
- Create secret/env variable file outside this folder so it can be accessed by other bots that need it
without have duplicates.
- Clean up project and remove unused code
- Revisit docker setup and make sure to set it up properly
