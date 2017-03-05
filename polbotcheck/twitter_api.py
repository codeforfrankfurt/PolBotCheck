import tweepy
import json
from keys import myauth
import pprint
import time

import db

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

def get_tweets(screen_name):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    tweets = []
    for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=screen_name, count=200).items()):
        tweets.append(tweet.text)
        retweets = get_retweets(tweet.id)
        db.saveRetweets(tweet, retweets)
    return tweets

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


if __name__ == "__main__":
    # example to get list all tweets (text)
    #tweets_save = True
    name = '@malechanissen'
    content = get_tweets(name)

#    if tweets_save == True:
#        with open('sample_tweets.json', 'w') as json_out:
#            json.dump(content, json_out)
#        print('samples have been saved')

    # example get user_ids of who retweeted tweet with specific id
    #retweeters_save = False
    #status_id = '837968136074891264'
    #retweets = get_retweets(status_id)
    #print(retweets)
    #
    #db.saveRetweets()
    #if retweeters_save == True:
    #    with open('retweeters.json', 'w') as json_out:
    #        json.dump(retweeters, json_out)

    # example to get all retweeters associated with an user
    # print(get_all_retweeters(screen_name=name))
