import tweepy
import logging
import time
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(filename='out.log', level=logging.INFO)
logger = logging.getLogger()

# Import config script used to create twitter API.
from config import create_api
api = create_api()



# Search for specific hastags and retweet when we find them.
def retweet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} -filter:retweets"
        tweets = api.search(q=search_query, lang ="en", tweet_mode='extended')
        for tweet in tweets:
            hashtags = [i['text'].lower() for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#') for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                if (set(hashtags) & set(need_hashtags)) and tweet.user.id != api.me().id:
                    # This allows us to add a comment 
                    # to a retweet using the url of the original tweet
                    api.update_status("Learn about #EndSARS https://twitter.com/{}/status/{}".format(tweet.user.screen_name, tweet.id))
                    logger.info(f"Retweeted tweet from {tweet.user.name}")
                    time.sleep(120)
            except tweepy.TweepError as e:
                logger.error("Error on retweet", exc_info=True)
    else:
        logger.error("Hashtag search terms needs to be of type list", exc_info=True)
        return

# def runBot():
while True:
    retweet_tweets_with_hashtag(api, ["opensource"])
    retweet_tweets_with_hashtag(api, ["hacktoberfest"])
    logger.info("Waiting...")
    time.sleep(240)

# if __name__ == "__main__":
#     runBot()
