import argparse
from datetime import datetime
import time
import tweepy

import botornotapi
import db
from config.keys import myauth
from config.test_candidates import SLUGS, SLUGS_TO_SKIP, FOLLOWER_LIMIT

AUTH = tweepy.OAuthHandler(myauth['consumer_key'], myauth['consumer_secret'])
AUTH.set_access_token(myauth['access_token'], myauth['access_token_secret'])
TWITTER_API = tweepy.API(AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,\
                         retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
            print('Warning: Rate limit reached! ' + timestamp)
            time.sleep(15 * 60)

def save_tweets_with_retweets(screen_name):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    for tweet in limit_handled(tweepy.Cursor(TWITTER_API.user_timeline, id=screen_name, count=200).items()):
        retweets = get_retweets(tweet.id)
        db.saveRetweets(tweet, retweets)



def save_followers_with_botness(account_handle):
    global TOTAL_FOLLOWERS_SKIPPED, TOTAL_FOLLOWERS_WITH_BOTNESS, TOTAL_FOLLOWERS_WITHOUT_BOTNESS
    user = TWITTER_API.get_user(account_handle)
    db.saveUser(user)
    timestamp = datetime.now()
    db.saveToImportLog(IMPORT_KEY, {
        'accounts': {
            account_handle: {
                'tw_followers_count': user.followers_count,
                'account_saved_at': timestamp.timestamp()
            }
        }
    })
    print(timestamp.strftime("%d.%m.%Y %H:%M:%S"))
    print("Saved user @%s, now getting the followers (twitter reported %d)  ..." % (account_handle, user.followers_count))

    followers = get_followers(account_handle)
    for follower in followers:
        follower_handle = follower.screen_name
        if db.hasFollower(fromName=follower_handle, toName=account_handle):
            TOTAL_FOLLOWERS_SKIPPED += 1
            db.saveToImportLog(IMPORT_KEY, {
                'accounts': {
                    account_handle: {
                        'followers_skipped': {follower_handle: 'existed'}
                    }
                },
                'followers_skipped': TOTAL_FOLLOWERS_SKIPPED
            })
            print("Already checked @" + follower_handle + " ... skipping for now.")
            continue
        follower_botness = botornotapi.get_bot_or_not("@" + follower_handle)
        if follower_botness is not None:
            db.saveFollower(user, follower, follower_botness)
            TOTAL_FOLLOWERS_WITH_BOTNESS += 1
            db.saveToImportLog(IMPORT_KEY, {
                'accounts': {
                    account_handle: {
                        'followers': {follower_handle: follower_botness['score']}
                    }
                },
                'followers_with_botness': TOTAL_FOLLOWERS_WITH_BOTNESS
            })
            print("Saved follower @%s for @%s with botness %d" % (follower_handle, account_handle, follower_botness['score'] * 100))
        else:
            TOTAL_FOLLOWERS_WITHOUT_BOTNESS += 1
            db.saveToImportLog(IMPORT_KEY, {
                'accounts': {
                    account_handle: {
                        'followers_without_botness': {follower_handle: None}
                    }
                },
                'followers_without_botness': TOTAL_FOLLOWERS_WITHOUT_BOTNESS
            })
            print("Botness is none for @" + follower_handle)

    # done with followers loop, save timestamp
    timestamp = datetime.now()
    db.saveToImportLog(IMPORT_KEY, {
        'accounts': {
            account_handle: {
                'ended_at': timestamp.timestamp()
            }
        }
    })


def get_retweets(tweet_id):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(timestamp)
    retweets = []
    for retweet in TWITTER_API.retweets(id=tweet_id, count=200):
        retweets.append(retweet)
    return retweets

def get_followers(screen_name):
    timestamp = datetime.now()
    log_doc = {
        'accounts': {
            screen_name: {
                'started_at': timestamp.timestamp()
            }
        }
    }
    db.saveToImportLog(IMPORT_KEY, log_doc)
    if FOLLOWER_LIMIT == 0:
        print("Get all followers for @" + screen_name)
    else:
        print("Get %d followers for @%s" % (FOLLOWER_LIMIT, screen_name))
    print(timestamp.strftime("%d.%m.%Y %H:%M:%S"))
    followers = []
    for user in limit_handled(tweepy.Cursor(TWITTER_API.followers, screen_name="@"+screen_name, count=200).items(FOLLOWER_LIMIT)):
        followers.append(user)
    return followers

# def get_all_retweeters(screen_name):
#     timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
#     print(timestamp)
#     all_retweeters = []
#     for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=screen_name, count=200).items()):
#         print(tweet.id)
#         retweeters = get_retweets(tweet.id)
#         # somehow get to retweeters
#         # all_retweeters.append(retweeters_per_tweet)
#     return all_retweeters


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='retrieve data from twitter and save to database')
    flags = ['tweets', 'followers']
    parser.add_argument('-t', '--tweets',       action='store_true', help='get tweets and retweets')
    parser.add_argument('-f', '--followers',    action='store_true', help='get followers and their botness')
    parser.add_argument('-b', '--both',         action='store_true', help='get both available entities')
    parser.add_argument('-a', '--all',          action='store_true', help='get all candidates')

    args = parser.parse_args()
    if not (args.tweets or args.followers or args.both):
        parser.error('No action requested, please see --help')

    if args.all:
        FOLLOWER_LIMIT = 0

    # the following globals are for logging purposes, IMPORT_KEY will be used to
    # log to the DB document with that _key
    IMPORT_KEY = db.saveNewImportLog('twitter')
    TOTAL_FOLLOWERS_SKIPPED = 0
    TOTAL_FOLLOWERS_WITH_BOTNESS = 0
    TOTAL_FOLLOWERS_WITHOUT_BOTNESS = 0

    if args.followers or args.both:
        log_doc = {'get_followers': {'limit': FOLLOWER_LIMIT}}
        db.saveToImportLog(IMPORT_KEY, log_doc)

    # Now do the actual work
    slugs_to_scan = db.get_all_candidate_slugs() if args.all else SLUGS
    for slug in slugs_to_scan:
        try:
            if slug in SLUGS_TO_SKIP:
                timestamp = datetime.now().timestamp()
                db.saveToImportLog(IMPORT_KEY, {'candidates_skipped': {slug: timestamp}})
                print(slug + " was skipped via SLUGS_TO_SKIP")
                continue
            candidate = db.get_candidate(slug)
            if 'twitter_handle' not in candidate:
                timestamp = datetime.now().timestamp()
                db.saveToImportLog(IMPORT_KEY, {'candidates_wo_twitter': {candidate['slug']: timestamp}})
                print(candidate["slug"] + " is missing a twitter handle")
                continue
            twitter_handle = candidate['twitter_handle']
            if args.both:
                save_tweets_with_retweets(twitter_handle)
                save_followers_with_botness(twitter_handle)
            elif args.tweets:
                save_tweets_with_retweets(twitter_handle)
            elif args.followers:
                save_followers_with_botness(twitter_handle)
        except tweepy.error.TweepError as ex:
            timestamp = datetime.now().timestamp()
            db.saveToImportLog(IMPORT_KEY, {'candidates_w_exception': {slug: {'at': timestamp, 'msg': str(ex)}}})
            print(slug + " raised exception: " + str(ex))

