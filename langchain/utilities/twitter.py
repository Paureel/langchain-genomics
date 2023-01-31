"""Util that calls WolframAlpha."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.utils import get_from_dict_or_env
import torch

import requests
import json
import pandas as pd
import tweepy

class TWITTERAPIWrapper(BaseModel):
    """Wrapper for Twitter.
    """

    wolfram_client: Any  #: :meta private:
    wolfram_alpha_appid: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        wolfram_alpha_appid = get_from_dict_or_env(
            values, "wolfram_alpha_appid", "WOLFRAM_ALPHA_APPID"
        )
        values["wolfram_alpha_appid"] = wolfram_alpha_appid

        try:
            import wolframalpha

        except ImportError:
            raise ImportError(
                "wolframalpha is not installed. "
                "Please install it with `pip install wolframalpha`"
            )
        client = wolframalpha.Client(wolfram_alpha_appid)

        values["wolfram_client"] = client

        # TODO: Add error handling if keys are missing
        return values
        
    # Python Script to Extract tweets of a
# particular Hashtag using Tweepy and Pandas
 
# import modules

 
# function to display data of each tweet
    # Python Script to Extract tweets of a
# particular Hashtag using Tweepy and Pandas
 
# import modules

 
# function to display data of each tweet
    def printtweetdata(n, ith_tweet):
            
            return(ith_tweet[7])
     
     
    # function to perform data extraction
    def scrape(words, date_since, numtweet):
            alltweets = {}
            # Creating DataFrame using pandas
            db = pd.DataFrame(columns=['username',
                                       'description',
                                       'location',
                                       'following',
                                       'followers',
                                       'totaltweets',
                                       'retweetcount',
                                       'text',
                                       'hashtags'])
     
            # We are using .Cursor() to search
            # through twitter for the required tweets.
            # The number of tweets can be
            # restricted using .items(number of tweets)
            tweets = tweepy.Cursor(api.search,
                                   words, lang="en",
                                   since_id=date_since,
                                   tweet_mode='extended').items(numtweet)
     
     
            # .Cursor() returns an iterable object. Each item in
            # the iterator has various attributes
            # that you can access to
            # get information about each tweet
            list_tweets = [tweet for tweet in tweets]
     
            # Counter to maintain Tweet Count
            i = 1
     
            # we will iterate over each tweet in the
            # list for extracting information about each tweet
            for tweet in list_tweets:
                    username = tweet.user.screen_name
                    description = tweet.user.description
                    location = tweet.user.location
                    following = tweet.user.friends_count
                    followers = tweet.user.followers_count
                    totaltweets = tweet.user.statuses_count
                    retweetcount = tweet.retweet_count
                    hashtags = tweet.entities['hashtags']
     
                    # Retweets can be distinguished by
                    # a retweeted_status attribute,
                    # in case it is an invalid reference,
                    # except block will be executed
                    try:
                            text = tweet.retweeted_status.full_text
                    except AttributeError:
                            text = tweet.full_text
                    hashtext = list()
                    for j in range(0, len(hashtags)):
                            hashtext.append(hashtags[j]['text'])
     
                    # Here we are appending all the
                    # extracted information in the DataFrame
                    ith_tweet = [username, description,
                                 location, following,
                                 followers, totaltweets,
                                 retweetcount, text, hashtext]
                    db.loc[len(db)] = ith_tweet
     
                    # Function call to print tweet data on screen
                    
                    alltweets[i] = printtweetdata(i, ith_tweet)
                    i = i+1
            return(alltweets)

    def run(self, query: str) -> str:
        """Run query through Twitter and parse result."""
        # Load Twitter
        

        consumer_key = "DxxIC44NXOHkXDpAQBgTv117W"
        consumer_secret = "NtQspyL7W0oZJQilbcYRYvpVDgGASqApRkHuSzd3PIrqDqX08P"
        access_key = "812351836145549312-CUu74Jlc1pgdCZd7fM3KfTljKnLOrek"
        access_secret = "JTxAR6e9sX1r35IdZFKD3gqaJuu9FGKw0Z5slaQ51BNKd"


        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        try:
            
            answer = scrape(query, "2023-01--20", 50)

        
            
        except:
            return "Twitter wasn't able to answer it"

        if answer is None or answer == "":
            # We don't want to return the assumption alone if answer is empty
            return "No good Twitter Result was found"
        else:
            return f"Answer: {answer}"
