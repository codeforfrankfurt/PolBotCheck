import argparse
import time
import tweepy

import botornotapi
import db
from config.keys import myauth
from config.test_candidates import SLUGS, FOLLOWER_LIMIT

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

def save_followers_with_botness(account_handle):
    followers = get_followers("@" + account_handle)
    user = TWITTER_API.get_user(account_handle)
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    print("Save user @%s and the followers (twitter reported %d)  ..." % (account_handle, user.followers_count))
    db.saveUser(user)
    for follower in followers:
        follower_handle = follower.screen_name
        if db.hasFollower(fromName=follower_handle, toName=account_handle):
            print("Already checked @" + follower_handle + " ... skipping for now.")
            continue
        follower_botness = botornotapi.get_bot_or_not("@" + follower_handle)
        if follower_botness is not None:
            db.saveFollower(user, follower, follower_botness)
            print("Saved follower @%s for @%s with botness %f" % (follower_handle, account_handle, follower_botness['score']))
        else:
            print("Botness is none for @" + follower_handle)

def get_retweets(tweet_id):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    retweets = []
    for retweet in TWITTER_API.retweets(id=tweet_id, count=200):
        retweets.append(retweet)
    return retweets

def get_followers(screen_name):
    print("Get %d followers for %s" % (FOLLOWER_LIMIT, screen_name))
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    followers = []
    for user in limit_handled(tweepy.Cursor(TWITTER_API.followers, screen_name=screen_name, count=200).items(FOLLOWER_LIMIT)):
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

    for slug in SLUGS:
        candidate = db.get_candidate(slug)
        twitter_handle = candidate['twitter_handle']
        if args.all:
            save_tweets_with_retweets(twitter_handle)
            save_followers_with_botness(twitter_handle)
        elif args.tweets:
            save_tweets_with_retweets(twitter_handle)
        elif args.followers:
            save_followers_with_botness(twitter_handle)
