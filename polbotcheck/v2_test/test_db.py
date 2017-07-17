from arango import ArangoClient

import db

if __name__ == "__main__":
    authoring_graph = db.getGraph("authoring")
    user_col = db.getVertexCollection(authoring_graph, "v2_users")
    tweets_col = db.getVertexCollection(authoring_graph, "v2_tweets")
    authoring_col = db.getEdgeDefinition(authoring_graph, "v2_authoring", ["v2_users"], ["v2_tweets"])
    # user_col.insert({'_key': 'user1', 'screen_name': 'User1'})
    # user_col.insert({'_key': 'user2', 'screen_name': 'User2'})
    # tweets_col.insert({'_key': 'tweet1', 'text': 't1'})
    # tweets_col.insert({'_key': 'tweet2', 'text': 't2'})
    authoring_col.insert({'_key':'13421322', '_to': 'v2_tweets/tweet2', '_from': 'v2_users/user2'})
    authoring_col.insert({'_key':'13421321', '_to': 'v2_tweets/tweet1', '_from': 'v2_users/user1'})
