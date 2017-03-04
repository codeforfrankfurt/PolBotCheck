####
#
#   get followers, classify them as bots, aggregate.
#
###





from __future__ import print_function
import json
import tweepy
import requests


consumer_key = 'i5sRKkw2Y9wPcIdKKf3nA'
consumer_secret = 'vfHWRFjsyfquUG7NJyTM45B3HaxzPgGlX3OTLR3IGeg'
access_key = '1277127895-8jHJzzuu53zpJP4Cf7YJIh3z3MYjHtveIWq0K4u'
access_secret = 'NlqlBsEgiyBTFqYajrpK4T8aP0csWe4mpterr8WFUFXs2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret )
twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

botornot_auth = { 'consumer_key': consumer_key, 'consumer_secret': consumer_secret, 'access_token': access_key, 'access_token_secret': access_secret }
bon = botornot.BotOrNot(**botornot_auth)

screen_name = '@clayadavis'

def get_botOrNot(screen_name):
    """  not functioning yet, due to problem with parser"""

    user_timeline = twitter_api.user_timeline(screen_name, count=200)

    if user_timeline:
        user_data = user_timeline[0]['user']
    else:
        user_data = twitter_api.get_user(screen_name)
    if not screen_name.startswith('@'):
        screen_name = '@' + screen_name
    search = twitter_api.search(screen_name, count=100)
    mentions = search['statuses']
    tweets = user_timeline + mentions
    post_body = {'content': tweets,
             'meta': {
                'user_id': user_data['id_str'],
                'screen_name': screen_name,
                },
            }

    bon_url = 'http://truthy.indiana.edu/botornot/api/1/check_account'
    bon_response = requests.post(bon_url, data=json.dumps(post_body))
    bon_response.status_code
    return(bon_response.json())

def get_bot_or_not(screen_name):
    """ returns bot or not features, using python package"""
    result = bon.check_account(screen_name)
    print(result)

def get_followers(screen_name):
    
    users = tweepy.Cursor(twitter_api.followers, screen_name=screen_name, count=200).items()
    #print(users)
    k=0
    followerlist =[]
    while True:  
        try:
            user = next(users)
        except tweepy.TweepError:
            time.sleep(60*15)
            user = next(users)
        except StopIteration:
            break
        followerlist.append("@" + user.screen_name)
    return followerlist
