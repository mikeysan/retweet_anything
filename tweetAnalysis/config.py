import tweepy
import os
import sys
from secrets import *

from dotenv import load_dotenv
load_dotenv()

import logging
CONSUMER_KEY = os.getenv('CKEY')
CONSUMER_SECRET = os.getenv('CSECRET')
ACCESS_TOKEN = os.getenv('ATOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ATOKEN_SECRET')

logger = logging.getLogger()


def create_api():
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET
    # consumer_key = key[0]
    # consumer_secret = key[1]
    # access_token = key[2]
    # access_token_secret = key[3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
