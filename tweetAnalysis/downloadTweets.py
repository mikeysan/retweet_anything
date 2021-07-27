from config import create_api
import tweepy
from textblob import TextBlob
import jsonpickle
import pandas as pd
import json
import logging
from config import create_api  # Import config script used to create twitter API.
api = create_api()

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename='analysis.log', level=logging.INFO)
logger = logging.getLogger()


searchQuery = 'LekkiMassacre OR endpolicebrutalitynow'
retweet_filter = '-filter:retweets'

q = searchQuery.lower() + retweet_filter
tweetsPerQry = 100
fName = 'lekki_tweets.txt'
sinceId = None

max_id = -1
maxTweets = 1000

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        tweets = []
        try:
            if max_id <= 0:
                if not sinceId:
                    new_tweets = api.search(q=q, lang="en", count=tweetsPerQry, tweet_mode='extended')

                else:
                    new_tweets = api.search(q=q, lang="en", count=tweetsPerQry,
                                        since_id=sinceId, tweet_mode='extended')
            else:
                if not sinceId:
                    new_tweets = api.search(q=q, lang="en", count=tweetsPerQry,
                                        max_id=str(max_id - 1), tweet_mode='extended')
                else:
                    new_tweets = api.search(q=q, lang="en", count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId, tweet_mode='extended')

            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(str(tweet.full_text.replace('\n', '').encode("utf-8"))+"\n")

            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break


print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
