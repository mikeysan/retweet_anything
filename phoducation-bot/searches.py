import tweepy
import logging
import time
import random
# import environment variables
from dotenv import load_dotenv
from datetime import datetime, timedelta
# Import config script used to create twitter API.
from config import create_api

load_dotenv()

logging.basicConfig(filename='searches_output.log', level=logging.INFO)
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def search_tweets(api):
    '''
        DESCRIPTION:
        We perform a search for various strings and retweet what we find.
    '''
    logger.info("Searching for tweets")
    query = ["fujifilm firmware update",
            "canon release new",
            "canon announced",
            "canon firmware update",
            "fujifilm release new",
            "fujifilm announced",
            "fujifilm announce",
            "nikon release new",
            "nikon announced",
            "nikon announce",
            "nikon firmware update",
            "sony release new",
            "sony announced",
            "sony announce",
            "sony firmware update"
            ]
    for i in query:
        tweets = api.search(q=i, lang="en", rpp=10)
        for tweet in tweets:
            try:
                if tweet.user.id != api.me().id:
                    api.retweet(tweet.id)
                    logger.info(f"Retweeted tweet from {tweet.user.name}")
                    time.sleep(25)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=True)
        # the code below simply displays the results
        # for tweet in api.search(q=i, lang="en", rpp=10):
        #     logger.info(f"Found {tweet.user.name}:{tweet.text}")
        #     print(f"{tweet.user.name}:{tweet.text}")


def main():
    api = create_api()
    while True:
        search_tweets(api)
        logger.info("Waiting...")
        time.sleep(240)

if __name__ == "__main__":
    main()
