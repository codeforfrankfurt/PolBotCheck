#/usr/bin/env python3

from arango import ArangoClient
from datetime import tzinfo

from db_credentials import db_credentials

# Configure your ArangoDB server connection here
conn = ArangoClient(protocol=db_credentials['protocol'], host=db_credentials['host'], port=db_credentials['port'], username=db_credentials['username'], password=db_credentials['password'])

dbName = 'polBotCheck'
if dbName not in conn.databases():
    db = conn.create_database(dbName)
db = conn.db(dbName)

def getCollection(collectionName, edge=False):
    collectionNames = map(lambda c: c['name'], db.collections())
    if collectionName not in collectionNames:
        db.create_collection(collectionName, edge=edge)
    return db.collection(collectionName)

def getVertexCollection(graph, collectionName):
    collectionNames = map(lambda c: c['name'], db.collections())
    if collectionName not in collectionNames:
        graph.create_vertex_collection(collectionName)
    return db.collection(collectionName)

def getGraph(graphName):
    graphNames = map(lambda g: g['name'], db.graphs())
    if graphName not in graphNames:
        db.create_graph(graphName)
    return db.graph(graphName)

def getEdgeDefinition(graph, edgeDefName, fromCollections, toCollections):
    definitionNames = map(lambda d: d['name'], graph.edge_definitions())
    if edgeDefName not in definitionNames:
        graph.create_edge_definition(
            name=edgeDefName,
            from_collections=fromCollections,
            to_collections=toCollections
        )
    return graph.edge_collection(edgeDefName)

# create the collections we need, if necessary
usersCol = getCollection('users')

followersGraph = getGraph('followers')
followersCol = getEdgeDefinition(followersGraph, 'followers', ['users'], ['users'])

retweetsGraph = getGraph('retweets')
tweetsCol = getVertexCollection(retweetsGraph, 'tweets')
retweetsCol = getEdgeDefinition(retweetsGraph, 'retweets', ['tweets'], ['tweets'])

def saveUser(user):
    if not usersCol.has(user):
        usersCol.insert({'_key': user})


def getUserEdgeDoc(fromName='', toName=''):
    if fromName != '':
        return {'_from': 'users/'+ fromName, '_to': 'users/' + toName}
    else:
        return {'_to': 'users/' + toName}

def getRetweetEdgeDoc(fromID='', toID=''):
    if fromID != '':
        return {'_from': 'tweets/'+ fromID, '_to': 'tweets/' + toID}
    else:
        return {'_to': 'tweets/' + toID}


def getUser(user):
    myuser = usersCol.find({'_key':user})
    try: 
        foundUser = next(myuser)
        return foundUser
    except:
        return None

def getFollowers(toName=''):
    return followersCol.find(getUserEdgeDoc(toName=toName))

def hasFollower(fromName='', toName=''):
    return followersCol.find(getUserEdgeDoc(fromName=fromName, toName=toName), None, 1).count() > 0

def hasRetweet(fromID='', toID=''):
    return retweetsCol.find(getRetweetEdgeDoc(fromID=fromID, toID=toID), None, 1).count() > 0

def saveFollower(username, follower, botness):
    doc = {'_key': follower.screen_name, 'botness': botness}
    doc['followerOf'+username] = follower._json
    if usersCol.has(doc['_key']):
        usersCol.update(doc)
    else:
        usersCol.insert(doc)
    
    if not hasFollower(fromName=follower.screen_name, toName=username):
        followersCol.insert(getUserEdgeDoc(fromName=follower.screen_name, toName=username))

def saveTweet(tweet):
    tweetDoc = {'_key': tweet.id_str}
    tweetDoc.update(tweet._json)
    if tweetsCol.has(tweet.id_str):
        tweetsCol.update(tweetDoc)
    else:
        tweetsCol.insert(tweetDoc)

def saveRetweets(tweet, retweets):
    saveTweet(tweet)
    for retweet in retweets:
        saveTweet(retweet)
        
        if not hasRetweet(fromID=tweet.id_str, toID=retweet.id_str):
            retweetsCol.insert(getRetweetEdgeDoc(fromID=tweet.id_str, toID=retweet.id_str))

def save_word_frequencies(user, word_cluster, force_write):
    myuser = usersCol.find({'_key': user})
    try: 
        found_user = next(myuser)
        if 'word_cluster' not in found_user or force_write:
            found_user['word_cluster'] = word_cluster
            usersCol.update(found_user)
    except:
        return None
