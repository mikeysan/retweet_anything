query = ["release", "firmware", "canon", "fujifilm", "nikon", "sony"]


tweets = api.search(q=i, lang="en", rpp=10)
for tweet in tweets:
    if tweet.user.id != api.me().id:
        api.retweet(tweet.id)
        logger.info(f"Retweeted tweet from {tweet.user.name}")
        time.sleep(25)