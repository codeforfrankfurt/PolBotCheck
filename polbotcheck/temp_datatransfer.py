import json
import tweepy
import requests
import botornotapi

from userlist import users
import db


for user in users:
    followerlist = botornotapi.get_followers(user)
    for follower in followerlist:
        botness = botornotapi.get_bot_or_not(follower)
        if botness is not None:
            db.saveFollower(user, botness)
            print("Saved follower " + follower['meta']['user_id'] + " for " + user)
        else
            print("Botness for " + user + " is none.")

