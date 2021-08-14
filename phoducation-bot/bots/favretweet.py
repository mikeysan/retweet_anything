import tweepy
import logging
import time
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__(api)
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
                time.sleep(100)
            except tweepy.TweepError:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                time.sleep(100)
            except tweepy.TweepError:
                logger.error("Error on fav and retweet", exc_info=True)


def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])


if __name__ == "__main__":
    main(["streetphotography",
          "travelphotograhy",
          "photographytips",
          "endsars",
          "endsarsnow"
          ])
