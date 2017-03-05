import json
import tweepy
import requests
import botornotapi

from userlist import users
import db


for user in users:
    followerlist = botornotapi.get_followers("@" + user)
    db.saveUser(user)
    for follower in followerlist:
        screenName = follower.screen_name
        if db.hasFollower(fromName=screenName, toName=user):
            print("Already checked " + screenName + " skipping for now.")
            next
        followerBotness = botornotapi.get_bot_or_not("@" + screenName)
        if followerBotness is not None:
            db.saveFollower(user, follower, followerBotness)
            print("Saved follower @" + screenName + " for @" + user)
        else:
            print("Botness for @" + screenName + " is none.")

