import argparse
import time
import tweepy

import botornotapi
import db
from config.keys import myauth
from config.userlist import USERS

AUTH = tweepy.OAuthHandler(myauth['consumer_key'], myauth['consumer_secret'])
AUTH.set_access_token(myauth['access_token'], myauth['access_token_secret'])
TWITTER_API = tweepy.API(AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,\
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
    for tweet in limit_handled(tweepy.Cursor(TWITTER_API.user_timeline, id=screen_name, count=200).items()):
        retweets = get_retweets(tweet.id)
        db.saveRetweets(tweet, retweets)

def save_followers_with_botness(user):
    followers = get_followers("@" + user)
    db.saveUser(user)
    for follower in followers:
        screen_name = follower.screen_name
        if db.hasFollower(fromName=screen_name, toName=user):
            print("Already checked @" + screen_name + " skipping for now.")
            continue
        follower_botness = botornotapi.get_bot_or_not("@" + screen_name)
        if follower_botness is not None:
            db.saveFollower(user, follower, follower_botness)
            print("Saved follower @" + screen_name + " for @" + user)
        else:
            print("Botness for @" + screen_name + " is none.")

def get_retweets(tweet_id):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    retweets = []
    for retweet in TWITTER_API.retweets(id=tweet_id, count=200):
        retweets.append(retweet)
    return retweets

def get_followers(screen_name):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    followers =[]
    for user in limit_handled(tweepy.Cursor(TWITTER_API.followers, screen_name=screen_name, count=200).items()):
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
    parser = argparse.ArgumentParser(description='retrieve data from twitter and save to database')
    flags = ['tweets', 'followers']
    parser.add_argument('-t', '--tweets', action='store_true', help='get tweets and retweets')
    parser.add_argument('-f', '--followers', action='store_true', help='get followers and their botness')
    parser.add_argument('-a', '--all', action='store_true', help='get all available entities')

    args = parser.parse_args()
    if not (args.tweets or args.followers or args.all):
        parser.error('No action requested, please see --help')

    for user in USERS:
        if args.all:
            save_tweets_with_retweets(user)
            save_followers_with_botness(user)
        elif args.tweets:
            save_tweets_with_retweets(user)
        elif args.followers:
            save_followers_with_botness(user)
