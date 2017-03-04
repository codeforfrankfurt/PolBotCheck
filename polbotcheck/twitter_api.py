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
            print('Warning: Rate limit reached!')
            time.sleep(15 * 60)

def get_content(screen_name):
    content = []
    for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=screen_name, count=200).items()):
        content.append(tweet.id)

        with open('sample_tweet.json', 'w') as json_out:
            json.dump(tweet._json, json_out)
        exit()
        print(tweet.id)
    return content

def get_retweeters(tweet_id):
    content = []
    for tweet in api.retweets(id=tweet_id, count=200):
        content.append((tweet._json['user']['screen_name'], tweet._json['user']['name']))

    return content

if __name__ == "__main__":
    # example to get list all tweets (text)
    tweets_save = False
    name = '@peteraltmaier'
    content = get_content(name)

    if tweets_save == True:
        with open('sample_tweets.json', 'w') as json_out:
            json.dump(content, json_out)

    # example get user_ids of who retweeted tweet with specific id
    retweeters_save = False
    status_id = '837968136074891264'
    retweeters = get_retweeters(status_id)
    if retweeters_save == True:
        with open('retweeters.json', 'w') as json_out:
            json.dump(retweeters, json_out)
