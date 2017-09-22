

# Replace my_* variables with your information
#
#
# To get these information you have to go to apps.twitter.com
# - create an app
# - generate Keys and Access Tokens
# - rename this file into keys.py
import os

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

myauth = { 'consumer_key': consumer_key, 'consumer_secret': consumer_secret, 'access_token': access_token, 'access_token_secret': access_token_secret }
