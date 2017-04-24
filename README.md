# PolBotCheck
Check political bots on social networks

The goal is to show information about politicians regarding who is retweeting their Twitter
tweets, if it is humans or bots.

We use information from [Truthy BotOrNot](http://truthy.indiana.edu/botornot/), a project
from Indiana University, which calculates a probability of a Twitter account being a bot
or a human. We check that on retweeters of a politician and calculate a score for each
topic (aka hashtag) he or she is talking about. This helps to identify, if a tweet is
really interesting to the public or if it is only interesting for certain bots.

The list of politicians was loaded from [Bundestwitter](http://www.bundestwitter.de).

## Installation and usage notes
### Backend

    cd polbotcheck
    cp keys-sample.py keys.py
    cp db_credentials-sample.py db_credentials.py
    pip install -r requirements.txt 
    python twitter_api.py --all

### Frontend

    cd web
    npm install
    npm start

_npm install_ is only needed the first time.

### Tips

 * Arango Server Commands:

    arangodump --server.endpoint tcp://disruptivepulse.com:6754 --server.username root --server.database polBotCheck --output-directory "dump"
    arangoimp --file SOMEFILE.json --server.endpoint tcp://disruptivepulse.com:6754 --server.username root --server.database polBotCheck --collection users --create-collection true


## Concepts definitions

*Follower*: twitter follower concept

*Engaged user*: User B is engaged with user A if user B retweets or likes user A
tweets.

*Audience*: the ensemble of the set of followers with the set of engaged users
in a specific topic or domain.

*Bot score*: belief on how much a user is a bot.

*Botness*: or bot level is a measure of the weighted ratio of believed bots in a
given entity (e.g. user's set of followers, or user's audience).
