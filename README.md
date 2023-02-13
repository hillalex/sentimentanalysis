# Scripts for scraping and analysing tweets 

## Requirements

* python3
* quarto - https://quarto.org/

Install Python requirements with:
```pip3 install -r requirement.txt```


## Gathering data

For 1. to authenticate with the Twitter API a valid [bearer token](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens) needs to be present as 
an environment variable named `TWITTER_BEARER_TOKEN`:

```export TWITTER_BEARER_TOKEN=<xxxxxxx>```

1. `get_tweets.py` - downloads 5 minutes worth of data from the Twitter API V2 sample stream, and 
all tweets with the keywords "pregnancy" and "childbirth" in the same period and stores in `data` folder in a timestamped subdirectory.
2. `analyse_sentiment.py` - runs `nltk` sentiment analyser on tweets gathered by 1. and stores combined data as csvs. 
Twitter isn't very good at returning a "lang" attribute, so also filter out non-English tweets here using `nlp` package.

## Analysis

WIP.

```quarto preview explore.qmd```
