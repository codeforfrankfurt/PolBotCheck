####
#
#   get followers, classify them as bots, aggregate.
#
###
from __future__ import print_function
import botornot
from config.keys import myauth

BOTORNOT_API = botornot.BotOrNot(**myauth)
def get_bot_or_not(screen_name):
    """ returns bot or not features, using python package"""
    try:
        result = BOTORNOT_API.check_account(screen_name)
    except Exception as err:
        print(err)
        return None
    return(result)
