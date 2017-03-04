import tweepy
import botornot

if __name__ == "__main__":

    consumer_key = 'fillout'
    consumer_secret = 'fillout'
    access_token = 'fillout'
    access_token_secret = 'fillout'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    user = api.get_user('@peteraltmaier')
    print('No. friend: {}'.format(user.screen_name))
    print(user.followers_count)
    friends = ', '.join(list([friend.screen_name for friend in user.friends()]))
    print('friends: {}'.format(friends))
    # for friend in user.friends():
    #     print(friend.screen_name)

    botornot_auth = { 'consumer_key': consumer_key, 'consumer_secret': consumer_secret, 'access_token': access_token, 'access_token_secret': access_token_secret }
    bon = botornot.BotOrNot(**botornot_auth)

    # Check a single account
    result = bon.check_account('@clayadavis')
    print(result)

    # Check a sequence of accounts
    # accounts = ['@clayadavis', '@onurvarol', '@jabawack']
    # results = list(bon.check_accounts_in(accounts))
