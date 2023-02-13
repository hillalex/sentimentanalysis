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


# First get 1% sample stream.
# The API doesn't allow filtering rules
# without a keyword so do some filtering here.
def on_tweet(tweet):
    # run for 15 minutes
    if time.time() - start_time > 60 * 15:
        client.disconnect()
    # exclude retweets
    if tweet.text.startswith("RT"):
        return
    # exclude replies
    if tweet.text.startswith("@"):
        return
    # exclude links
    if "https://" in tweet.text:
        return
    data.append(tweet.data)


client = tweepy.StreamingClient(bearer_token)
client.on_tweet = on_tweet
client.sample(tweet_fields="created_at")


data_dir = "data/{}".format(start_datetime.strftime("%Y-%m-%d-%H:%M:%S"))
os.makedirs(data_dir)
with open("{}/alltweets.json".format(data_dir), "w") as f:
    json.dump(data, f)

# Now get all tweets with keywords from the same time period
# excluding RTs, links and replies
preg_data = search_tweets(build_url("(pregnancy OR childbirth) -is:retweet  -is:reply -has:links"),
                          start_datetime)

with open("{}/pregnancytweets.json".format(data_dir), "w") as f:
    json.dump(preg_data, f)
