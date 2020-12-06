import tweepy
import logging
import time
import random
from datetime import datetime, timedelta

logging.basicConfig(filename='out.log', level=logging.INFO)
logger = logging.getLogger()

# Import config script used to create twitter API.
from config import create_api
api = create_api()



def retweet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} -filter:retweets"
        tweets = api.search(q=search_query, lang ="en", tweet_mode='extended')
        for tweet in tweets:
            hashtags = [i['text'].lower() for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#') for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                if set(hashtags) & set(need_hashtags):
                    if tweet.user.id != api.me().id and not tweet.retweeted:
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        time.sleep(15)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=True)
                continue
    else:
        logger.error("Hashtag search terms needs to be of type list", exc_info=True)
        return

# We can test this with a number of hashtags..
while True:
        retweet_tweets_with_hashtag(api, ["cityjsconf", "cityjs", "github", "hacktoberfest"])
        logger.info("Waiting...")
        time.sleep(120)
