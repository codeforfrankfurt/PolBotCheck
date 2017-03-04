####
#
#   get followers, classify them as bots, aggregate.
#
###





from __future__ import print_function
import json
import tweepy
import requests
import botornot
import time
from keys import myauth


auth = tweepy.OAuthHandler(myauth['consumer_key'], myauth['consumer_secret'])
auth.set_access_token(myauth['access_token'], myauth['access_token_secret'] )
twitter_api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True,\
                         retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
bon = botornot.BotOrNot(**myauth)

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
    try:
        result = bon.check_account(screen_name)
        except Exception as err:
            print(err)
            return None
#    except botornot.NoTimelineError:
#        return None
#    except tweepy.TweepError:
#        return None
#    except StopIteration:
#        return None

    return(result)

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
        followerlist.append(user)
    return followerlist

