#/usr/bin/env python3

from pyArango.connection import *
from pyArango.database import *
from pyArango.collection import *
from pyArango.document import *
from pyArango.query import *
from pyArango.graph import *
from pyArango.theExceptions import *

# Configure your ArangoDB server connection here
conn = Connection(arangoURL="http://192.168.42.152:8529", username="root", password="Qf5sc1ZOltQ7z4ab")

db = None
edgeCols = {}
followersCol = {}

# we create our own database so we don't interfere with userdata:
dbName = "polBotCheck"
if not conn.hasDatabase(dbName):
    db = conn.createDatabase(dbName)
else:
    db = conn[dbName]

collectionName = "followers"
if not db.hasCollection(collectionName):
    followersCol = db.createCollection('Collection', name=collectionName)
else:
    followersCol = db.collections[collectionName]

def saveFollower(follower):
    doc = {"_key": follower["meta"]["user_id"]}
    doc.update(follower)
    followersCol.createDocument(doc).save()

follower = {'meta': {'screen_name': 'username', 'user_id': '1277127895'}, 'score': 0.37, 'categories': {'languageagnostic_classification': 0.33, 'friend_classification': 0.15, 'network_classification': 0.31, 'temporal_classification': 0.51, 'user_classification': 0.22, 'sentiment_classification': 0.5, 'content_classification': 0.6033333333333334}}
saveFollower(follower)
