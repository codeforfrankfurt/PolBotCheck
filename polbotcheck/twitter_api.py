import tweepy
import json
from keys import myauth
import pprint
import time

import db
import botornotapi
from userlist import USERS

auth = tweepy.OAuthHandler(myauth['consumer_key'], myauth['consumer_secret'])
auth.set_access_token(myauth['access_token'], myauth['access_token_secret'] )
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True,\
                         retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
            print('Warning: Rate limit reached! ' + timestamp)
            time.sleep(15 * 60)

def save_tweets_with_retweets(screen_name):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    tweets = []
    for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=screen_name, count=200).items()):
        tweets.append(tweet.text)
        retweets = get_retweets(tweet.id)
        db.saveRetweets(tweet, retweets)

def save_followers_with_botness(user):
    followers = get_followers("@" + user)
    db.saveUser(user)
    for follower in followers:
        screenName = follower.screen_name
        if db.hasFollower(fromName=screenName, toName=user):
            print("Already checked @" + screenName + " skipping for now.")
            continue
        followerBotness = botornotapi.get_bot_or_not("@" + screenName)
        if followerBotness is not None:
            db.saveFollower(user, follower, followerBotness)
            print("Saved follower @" + screenName + " for @" + user)
        else:
            print("Botness for @" + screenName + " is none.")

def get_retweets(tweet_id):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    retweets = []
    for retweet in api.retweets(id=tweet_id, count=200):
        retweets.append(retweet)
    return retweets

def get_followers(screen_name):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    followers =[]
    for user in limit_handled(tweepy.Cursor(twitter_api.followers, screen_name=screen_name, count=200).items()):
        followers.append(user)
    return followers

# def get_all_retweeters(screen_name):
#     timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
#     print(timestamp)
#     all_retweeters = []
#     for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=screen_name, count=200).items()):
#         print(tweet.id)
#         retweeters = get_retweets(tweet.id)
#         # somehow get to retweeters
#         # all_retweeters.append(retweeters_per_tweet)
#     return all_retweeters


if __name__ == "__main__":
    for user in USERS:
        save_tweets_with_retweets(user)
        save_followers_with_botness(user)
