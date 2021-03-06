#/usr/bin/env python3

import argparse
import json
from datetime import datetime
import time
from arango import ArangoClient

from config.db_credentials import db_credentials

CANDIDATES_PATH = '../web/public/candidates.json'


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

def convertToKey(twitterHandle):
    return twitterHandle and twitterHandle.lower()

# create the collections we need, if necessary
usersCol = getCollection('users')
candidatesCol = getCollection('candidates')
districtsCol = getCollection('districts')
importLogsCol = getCollection('importLogs')

followersGraph = getGraph('followers')
followersCol = getEdgeDefinition(followersGraph, 'followers', ['users'], ['users'])

retweetsGraph = getGraph('retweets')
tweetsCol = getVertexCollection(retweetsGraph, 'tweets')
retweetsCol = getEdgeDefinition(retweetsGraph, 'retweets', ['tweets'], ['tweets'])

def saveUser(user, botness=None):
    key = convertToKey(user.screen_name)
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    doc = {'_key': key, 'scraped_at': timestamp}

    # save the user data from twitter in its own subdoc to separate it from our stuff
    doc['twitter'] = user._json

    if botness is not None:
        doc['botness'] = botness

    if usersCol.has(key):
        usersCol.update_match({"_key": key}, doc)
    else:
        usersCol.insert(doc)


def getUserEdgeDoc(fromName='', toName=''):
    if fromName != '':
        return {'_from': 'users/' + convertToKey(fromName), '_to': 'users/' + convertToKey(toName)}
    else:
        return {'_to': 'users/' + convertToKey(toName)}

def getRetweetEdgeDoc(fromID='', toID=''):
    if fromID != '':
        return {'_from': 'tweets/'+ fromID, '_to': 'tweets/' + toID}
    else:
        return {'_to': 'tweets/' + toID}


def getUser(twitter_handle):
    myuser = usersCol.find({'_key': convertToKey(twitter_handle)})
    try: 
        foundUser = next(myuser)
        return foundUser
    except StopIteration:
        return None


def getFollowers(toName=''):
    cursor = db.aql.execute(
        "FOR vertex, edge IN INBOUND 'users/" + toName + "' GRAPH 'followers'" +
        "RETURN {id: vertex._id, botness: vertex.botness}"
    )
    return cursor


def getFollowerStats(toName=''):
    try:
        cursor = getFollowers(toName)
    except:
        cursor = []

    numHumans = 0
    numBots = 0
    for follower in cursor:
        if follower["botness"]["score"] >= 0.7:
            numBots += 1
        else:
            numHumans += 1
    return {
        "numHumans": numHumans,
        "numBots": numBots
    }

def hasFollower(fromName='', toName=''):
    return followersCol.find(getUserEdgeDoc(fromName=fromName, toName=toName), None, 1).count() > 0

def hasRetweet(fromID='', toID=''):
    return retweetsCol.find(getRetweetEdgeDoc(fromID=fromID, toID=toID), None, 1).count() > 0

def saveFollower(user, follower, botness):
    # save the follower as a user vertex
    saveUser(follower, botness)

    # and the user-follower edge
    user_name = user.screen_name
    follower_name = follower.screen_name
    if not hasFollower(fromName=follower_name, toName=user_name):
        followersCol.insert(getUserEdgeDoc(fromName=follower_name, toName=user_name))


def saveNewImportLog(import_type):
    """
    :param import_type: twitter or file name
    :type import_type: String
    :return : value of DB key of that import
    """
    result = importLogsCol.insert({"created_at": datetime.now().timestamp(), "import_type": import_type})
    return result['_key']


def saveToImportLog(key, doc_to_save):
    importLogsCol.update_match({"_key": key}, dict(updated_at=datetime.now().timestamp(), **doc_to_save))


def saveTweet(tweet):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    tweetDoc = {'_key': tweet.id_str, 'scraped_at': timestamp}

    # save the actual tweet in its own subdoc to separate it from our stuff
    tweetDoc['twitter'] = tweet._json
    if tweetsCol.has(tweet.id_str):
        tweetsCol.update_match({"_key": tweetDoc['_key']}, tweetDoc)
    else:
        tweetsCol.insert(tweetDoc)

def saveRetweets(tweet, retweets):
    saveTweet(tweet)
    for retweet in retweets:
        saveTweet(retweet)

        if not hasRetweet(fromID=tweet.id_str, toID=retweet.id_str):
            retweetsCol.insert(getRetweetEdgeDoc(fromID=tweet.id_str, toID=retweet.id_str))

def save_word_frequencies(user_name, word_frequencies):
    user = usersCol.get(user_name)
    if user is not None:
        user['word_frequencies'] = word_frequencies
        usersCol.update(user, merge=False)

def get_districts():
    cursor = db.aql.execute(
        "FOR d IN %s SORT d.name ASC RETURN d" % districtsCol.name
    )
    return cursor


def get_district(number):
    if number == None:
        number = '0'
    return districtsCol.get(str(number))


def get_candidate(slug):
    candidate = candidatesCol.find({'_key': slug})
    try:
        doc = next(candidate)
        for link in doc['links']:
            if link["type"] == "twitter":
                doc['twitter_handle'] = link["id"]
        return doc
    except StopIteration:
        return None


def get_candidates_grouped_by_district():
    cursor = db.aql.execute(
        '''
        FOR c IN %s
            COLLECT district = c.election.district INTO candidateByDistrict
            RETURN {
                district,
                candidates: ( FOR temp IN candidateByDistrict SORT candidateByDistrict.d.election.list ASC RETURN {id: temp.c._key, election: temp.c.election} )
            }
        '''[1:-1] % candidatesCol.name
    )
    return cursor


def get_candidates_by_district(district):
    if district == "0":
        district = None
    else:
        district = int(district)
    query = '''
        FOR candidate IN %s
            FILTER candidate.election.district == @district
            SORT candidate.name.surname ASC
            RETURN candidate
        '''[1:-1] % candidatesCol.name
    cursor = db.aql.execute(query, bind_vars={'district': district})
    return cursor


def get_candidates_by_party(party):
    query = '''
        FOR candidate IN %s
            FILTER candidate.election.party == @party
            SORT candidate.name.surname ASC
            RETURN candidate
        '''[1:-1] % candidatesCol.name
    cursor = db.aql.execute(query, bind_vars={'party': party})
    return cursor


def get_all_candidate_slugs():
    slugs = []
    cursor = candidatesCol.all()
    for candidate in cursor:
        slugs.append(candidate["slug"])
    return slugs
    
def save_candidate(candidate):
    candidateDoc = {'_key': candidate['slug']}
    candidateDoc.update(candidate)

    if candidatesCol.has(candidate['slug']):
        candidatesCol.update_match({'_key': candidate['slug']}, candidateDoc)
    else:
        candidatesCol.insert(candidateDoc)


def import_candidates(filters):
    with open(CANDIDATES_PATH) as candidatesFile:
        json_data = json.load(candidatesFile)
    count = 0
    is_filtered = len(filters) > 0
    for candidate in json_data:
        matches_filter = filters.items() <= candidate['election'].items()
        if is_filtered and not matches_filter:
            print("Skipping ", candidate['slug'])
            next
        save_candidate(candidate)
        count += 1
    print("Imported %i candidates" % count)


def import_districts():
    with open(CANDIDATES_PATH) as candidatesFile:
        json_data = json.load(candidatesFile)
    for candidate in json_data:
        identifier = candidate['election']['district']
        name = None
        if identifier is None:
            identifier = 0
            name = 'Landesliste'
        identifier = str(identifier)

        if not districtsCol.has(identifier):
            print('Import ' + str(identifier))
            districtsCol.insert({'_key': identifier, 'name': name})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Methods to save to and read from the database')
    parser.add_argument('-he', '--hessian', action='store_true', help='import hessian candidates')
    parser.add_argument('-a', '--all', action='store_true', help='import all candidates')
    parser.add_argument('-d', '--districts', action='store_true', help='import all districts')

    args = parser.parse_args()
    if not (args.hessian or args.all or args.districts):
        parser.error('No action requested, please see --help')

    if args.all:
        import_candidates({})
    elif args.hessian:
        import_candidates({"state": "he"})
    elif args.districts:
        import_districts()
