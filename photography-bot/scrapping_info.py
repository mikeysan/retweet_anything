import logging
import tweepy
from datetime import datetime
import json
import pandas as pd
import csv
import re
from textblob import TextBlob
import string
import preprocessor as p
import os
import time
from dotenv import load_dotenv
from config import create_api

load_dotenv()

logging.basicConfig(filename='scrapping.log', level=logging.INFO)
logger = logging.getLogger()

startAPI = create_api()


def scraptweets(s_words, d_since, n_tweets, n_runs):
    api = startAPI
    # Define a for-loop to generate tweets at regular intervals
    # We cannot make large API calls in one go. Hence, let's try T times

    # Define a pandas dataframe to store the date:
    db_tweets = pd.DataFrame(columns=['username', 'acctdesc', 'location', 'following',
                                      'followers', 'totaltweets', 'usercreatedts', 'tweetcreatedts',
                                      'retweetcount', 'text', 'hashtags']
                             )
    program_start = time.time()
    for i in range(0, n_runs):
        # We will time how long it takes to scrape tweets for each run:
        start_run = time.time()

        # Collect tweets using the Cursor object
        # .Cursor() returns object that you can loop over to access the data collected.
        # Each item in the iterator has various attributes that you can access
        # to get information about each tweet
        tweets = tweepy.Cursor(api.search, q=s_words, lang="en", since=d_since, tweet_mode='extended').items(
            n_tweets)
        # Store these tweets into a python list
        tweet_list = list(tweets)
        # Obtain the following info (methods to call them out):
        # user.screen_name - twitter handle
        # user.description - description of account
        # user.location - where is he tweeting from
        # user.friends_count - no. of other users that user is following (following)
        # user.followers_count - no. of other users, following this user (followers)
        # user.statuses_count - total tweets by user
        # user.created_at - when the user account was created
        # created_at - when the tweet was created
        # retweet_count - no. of retweets
        # (deprecated) user.favourites_count -
        # probably total no. of tweets that is favourited by user
        # retweeted_status.full_text - full text of the tweet
        # tweet.entities['hashtags'] - hashtags in the tweet

        # Begin scraping the tweets individually:
        n_tweets = 0
        for tweet in tweet_list:
            # Pull the values
            username = tweet.user.screen_name
            acctdesc = tweet.user.description
            location = tweet.user.location
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            usercreatedts = tweet.user.created_at
            tweetcreatedts = tweet.created_at
            retweetcount = tweet.retweet_count
            hashtags = tweet.entities['hashtags']
            try:
                text = tweet.retweeted_status.full_text
            except AttributeError:  # Not a Retweet
                text = tweet.full_text
            # Add the 11 variables to the empty list - ith_tweet:
            ith_tweet = [username, acctdesc, location, following, followers, totaltweets,
                         usercreatedts, tweetcreatedts, retweetcount, text, hashtags]
            # Append to dataframe - db_tweets
            db_tweets.loc[len(db_tweets)] = ith_tweet
            # increase counter - numtweets
            n_tweets += 1

            # Run ended:
            end_run = time.time()
            duration_run = round((end_run - start_run) / 60, 2)

            print('no. of tweets scraped for run {} is {}'.format(i + 1, n_tweets))
            print('time taken for {} run to complete is {} mins'.format(i + 1, duration_run))

            time.sleep(920)  # 15 minute sleep time
            # Once all runs have completed, save them to a single csv file:
            # Obtain timestamp in a readable format
            to_csv_timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')
            # Define working path and filename
            path = os.getcwd()
            filename = path + '/data/' + to_csv_timestamp + 'lekki_tweets.csv'
            # Store dataframe in csv with creation date timestamp
            db_tweets.to_csv(filename, index=False)

            program_end = time.time()
            program_difference = program_end - program_start
            time_taken = round(program_difference / 60)
            print('Scraping has completed!')
            print('Total time taken to scrap is {} minutes.'.format(time_taken))


# Initialise these variables:
search_words = "#LekkiMassacre OR #endsars OR #endpolicebrutalitynow"
date_since = "2021-05-01"
numTweets = 2000
numRuns = 6


# Call the function scraptweets
scraptweets(search_words, date_since, numTweets, numRuns)
