

import json
import tweepy
import requests
import botornotapi

import db


for user in userlist:
    followerlist = botornotapi.get_followers(user)
    for follower in followerlist:
        botness = botornotapi.get_bot_or_not(follower)
        if botness is not None:
            db.saveFollower(botness)


