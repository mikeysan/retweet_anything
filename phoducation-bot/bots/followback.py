import tweepy
import logging
from config import create_api
import time

logging.basicConfig(filename='out.log', level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api, date_since):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers, since=date_since).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()

def main():
    api = create_api()
    date_since = "2020-10-01"
    while True:
        follow_followers(api, date_since)
        logger.info("Waiting...")
        time.sleep(120)

if __name__ == "__main__":
    main()