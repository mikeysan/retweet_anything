
import tweepy
import logging
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

logging.basicConfig(filename='out.log', level=logging.INFO)
logger = logging.getLogger()

# Import config script used to create twitter API.
from config import create_api
api = create_api()

# Lke and retweet a specific person's tweets
def fav_retweet_user(api, user_handle):
    search_query = f"{user_handle} -filter:retweets"
    logger.info(f'Retrieving tweets mentioning {user_handle}...')
    tweets = api.search(q=search_query, lang ="en")
    for tweet in tweets:
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
                logger.info(f"Liked a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                logger.info(f"Retweeted a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)


def play():
    while True:
        # fav_retweet_user(api, "@falzthebahdguy")
        # logger.info("Waiting...")
        # time.sleep(150)
        fav_retweet_user(api, "@fashionsfinest")
        logger.info("waiting...")
        time.sleep(150)
        fav_retweet_user(api, "@eddiejaoude")
        logger.info("Waiting...")
        time.sleep(150)


if __name__ == "__main__":
    play()