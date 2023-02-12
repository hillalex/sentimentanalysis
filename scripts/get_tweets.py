import os
import tweepy
import json
import time
import datetime

from search_tweets import search_tweets, build_url

data = []
start_time = time.time()
start_datetime = datetime.datetime.now()

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")


# first get 1% sample stream
def on_tweet(tweet):
    # run for 10 minutes
    if time.time() - start_time > 5 * 60:
        client.disconnect()
    if tweet.text.startswith("RT"):
        return
    data.append(tweet.data)


client = tweepy.StreamingClient(bearer_token)
client.on_tweet = on_tweet
client.sample(tweet_fields="created_at")

with open("../data/alltweets.json", "w") as f:
    json.dump(data, f)

# now get all tweets with keywords from the same time period
preg_data = search_tweets(build_url("(pregnancy OR pregnant OR childbirth) -is:retweet"), start_datetime)

with open("../data/pregnancytweets.json", "w") as f:
    json.dump(preg_data, f)
