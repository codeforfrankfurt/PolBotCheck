import json
import tweepy
import requests
import botornotapi

from userlist import users
import db


for user in users:
    followerlist = botornotapi.get_followers(user)
    for follower in followerlist:
        followerBotness = botornotapi.get_bot_or_not("@" + follower.screen_name)
        if followerBotness is not None:
            db.saveFollower(user, follower, botness)
            print("Saved follower " + follower['meta']['user_id'] + " for " + user)
        else
            print("Botness for " + user + " is none.")

