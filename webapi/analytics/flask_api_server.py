from flask import Flask, jsonify
from flask_cors import CORS

import db
import json

######################### FLASK APP
app = Flask(__name__)
CORS(app)


@app.route("/pbc")
def index():
    return [[row['election']['district'],row['election'],row['slug']] for row in candidates]


def get_full_name(name):
    if not name:
        return None
    full_name = ''
    if name['titles']:
        full_name = full_name + name['titles']
    if name['forename']:
        full_name = full_name + ' ' + name['forename']
    if name['surname']:
        full_name = full_name + ' ' + name['surname']
    if name['affix']:
        full_name = full_name + ' ' + name['affix']
    return full_name

@app.route("/pbc/getslugs")
def get_slugs():
    return [row['slug'] for row in candidates]

def get_candidate_by_slug(slug)
    if not slug:
        return None
    return list(filter(lambda x: x['slug']==slug,candidates))

@app.route("/pbc/user/<slug>")
def candidate_info(slug=None):
    """
    """
    if slug is None:
        return "Candidate not provided"

    candidate = db.get_candidate(slug)
    if candidate is None:
        return "Candidate not found"

    full_name = get_full_name(candidate['name'])

    twitter_user = db.getUser(candidate['twitter_handle'])
    if twitter_user is None:
       return "Twitter user for candidate lost in the dark forest - make a donation to us to find this user."

    followers = {"numFollowers": twitter_user["twitter"]["followers_count"]}
    follower_stats = db.getFollowerStats(candidate['twitter_handle'])
    followers.update(follower_stats)

    json_output = {
        "content": "MEMBER", 
        "member":{
            "name" : full_name,
            "pictureURL": '',
            "party": candidate["election"]["party"],
            "twitter_handle": candidate['twitter_handle']
        },
        "wordCluster": twitter_user.get("word_frequencies"),
        "followers": followers,
        "retweets": {
              "numRetweets": 12,
              "numHumans": 11,
              "numBots": 1
            },
        "retweeters": {
              "numRetweeters": 22,
              "numHumans": 9,
              "numBots": 13
            },
        "election": get_candidate_by_slug(slug)['election'],
        "botness": twitter_user["botness"] if "botness" in twitter_user else {}
    }

    return jsonify(json_output)

candidates=[]
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6755)
    candidates = json.load(open("../../web/public/candidates.json"))
