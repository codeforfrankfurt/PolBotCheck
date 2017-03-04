####
#
#   get followers, classify them as bots, aggregate.
#
###





from __future__ import print_function
import json
import tweepy
import requests

auth = tweepy.OAuthHandler('consumer_key', 'consumer_secret')
auth.set_access_token()

twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())



screen_name = '@clayadavis'

def get_botOrNot(screen_name):
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

