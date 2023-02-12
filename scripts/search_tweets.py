import os
import requests

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")


def build_url(query):
    def paged_url(next_token):
        url = "https://api.twitter.com/2/tweets/search/recent?max_results=100&tweet.fields=created_at&&query={}".format(
            query)
        if next_token is not None:
            url = url + "&pagination_token={}".format(next_token)
        return url

    return paged_url


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        return None
    return response.json()


def search_tweets(url_generator, start_datetime):
    url = url_generator(None)
    json_response = connect_to_endpoint(url)
    data = json_response["data"]
    while data[0]["created_at"] > start_datetime.strftime("%a %b %d %H:%M:%S +0000 %Y"):
        next_token = json_response["meta"]["next_token"]
        url = url_generator(next_token)
        json_response = connect_to_endpoint(url)
        if json_response is not None:
            data = data + json_response["data"]
        else:
            break
    return data
