#!/Users/mikeysan/.pyenv/shims/python

import tweepy
import logging
import time
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

logging.basicConfig(filename='out.log', level=logging.INFO)
logger = logging.getLogger()

# Import config script used to create twitter API.
from config import create_api
api = create_api()

# Like and retween mentions (of me)
def fav_retweet(api):
    logger.info('Retrieving tweets...')
    mentions = api.mentions_timeline(tweet_mode = 'extended')
    for mention in reversed(mentions):
        if mention.in_reply_to_status_id is not None or mention.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return

        if not mention.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                mention.favorite()
                logger.info(f"Liked tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)

        if not mention.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                mention.retweet()
                logger.info(f"Retweeted tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

# Search for specific hastags and retweet when we find them.
def retweet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} -filter:retweets"
        tweets = api.search(q=search_query, lang ="en", tweet_mode='extended', encoding="utf-8")
        for tweet in tweets:
            hashtags = [i['text'].lower() for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#') for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                if set(hashtags) & set(need_hashtags):
                    if tweet.user.id != api.me().id:
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        time.sleep(90)
            except tweepy.TweepError as e:
                logger.error("Error on retweet", exc_info=True)
    else:
        logger.error("Hashtag search terms needs to be of type list", exc_info=True)
        return

# Retweet any tweets with a certain Ticker (Stock Market Ticker)
# def retweet_tweets_with_ticker(api, need_ticker):
#     if type(need_ticker) is list:
#         search_query = f"{need_ticker} -filter:retweets"
#         tweets = api.search(q=search_query, lang ="en", tweet_mode='extended')
#         for tweet in tweets:
#             ticker = [i['text'].lower() for i in tweet.__dict__['entities']['symbols']]
#             try:
#                 need_ticker = [hashtag.strip('$') for hashtag in need_ticker]
#                 need_ticker = list(need_ticker)
#                 if set(ticker) & set(need_ticker):
#                     if tweet.user.id != api.me().id:
#                         api.retweet(tweet.id)
#                         logger.info(f"Retweeted tweet from {tweet.user.name}")
#                         time.sleep(15)
#             except tweepy.TweepError:
#                 logger.error("Error on retweet", exc_info=True)
#     else:
#         logger.error("Hashtag search terms needs to be of type list", exc_info=True)
#         return



# Testing like and retweet 
while True:
    fav_retweet(api)
    retweet_tweets_with_hashtag(api, ["github"])
    time.sleep(10)
    retweet_tweets_with_hashtag(api, ["cybersecurity"])
    time.sleep(10)
    retweet_tweets_with_hashtag(api, ["opensource"])
    logger.info("Waiting...")
    time.sleep(50)


# trying to figure out a way to add a comment as I tweet; i.e. retweet with comment
# only option I have found is to use the ful url of the original tweet
# api.update_status("My reaction https://twitter.com/screenname/status/123456789")
# Possible example
# api.update_status("@user1 @user2 https://twitter.com/{}/status/{}".format(tweet.user.screen_name, tweet.id))
# additional options may include using "attachment_url"
# i.e. api.update_status("@user1 @user2", attachment_url="url to original tweet")
# tweet.permalink - Permalink of tweet itself


#MLH #LocalHackDay #EddieHub