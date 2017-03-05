import tweepy
import json
from keys import myauth
import pprint
import time

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
            print('Warning: Rate limit reached!' + timestamp)
            time.sleep(15 * 60)

def get_tweets(screen_name):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    content = []
    for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=screen_name, count=200).items()):
        content.append(tweet.text)
        retweeters = get_retweeters(tweet.id)
    return content

# def get_all_retweeters(screen_name):
#     timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
#     print(timestamp)
#     all_retweeters = []
#     for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=screen_name, count=200).items()):
#         print(tweet.id)
#         retweeters_per_tweet = get_retweeters(tweet.id)
#         all_retweeters.append(retweeters_per_tweet)
#     return all_retweeters

def get_retweeters(tweet_id):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    content = []
    for tweet in api.retweets(id=tweet_id, count=200):
        # maybe return tweet._json['user'] instead of screen_name and name
        content.append((tweet._json['user']['screen_name'], tweet._json['user']['name']))
    return content


if __name__ == "__main__":
    # example to get list all tweets (text)
    tweets_save = True
    name = '@quentzer32'
    content = get_tweets(name)

    if tweets_save == True:
        with open('sample_tweets.json', 'w') as json_out:
            json.dump(content, json_out)
        print('samples have been saved')

    # example get user_ids of who retweeted tweet with specific id
    # retweeters_save = False
    # status_id = '837968136074891264'
    # retweeters = get_retweeters(status_id)
    # print(retweeters)
    # if retweeters_save == True:
    #     with open('retweeters.json', 'w') as json_out:
    #         json.dump(retweeters, json_out)

    # example to get all retweeters associated with an user
    # print(get_all_retweeters(screen_name=name))
