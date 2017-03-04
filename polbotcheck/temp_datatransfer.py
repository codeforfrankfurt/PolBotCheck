

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
            botness['polit']=user  #or any other key, cant think right now
            db.saveFollower(botness)


