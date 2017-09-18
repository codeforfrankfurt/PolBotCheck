from flask import Flask, jsonify
from flask_cors import CORS

import db

######################### FLASK APP
app = Flask(__name__)
CORS(app)

@app.route("/pbc")
def index():
    """
    Return organizational entities like Landesliste Hessen and the hessian election districts
    as well as the candidates in them
    """
    groupings = []
    candidates_by_district = db.get_candidates_by_district()
    for group in candidates_by_district:
        print(group)
        groupings.append(group)
    return jsonify({'candidates_by_district': groupings})


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
        "member": {
            "name": full_name,
            "pictureURL": '',
            "party": candidate["election"]["party"],
            "twitter_handle": candidate['twitter_handle']
        },
        "wordCluster": twitter_user.get("word_frequencies") or {'topics': []},
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
        "election": candidate['election'],
        "botness": twitter_user["botness"] if "botness" in twitter_user else {}
    }

    return jsonify(json_output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6755)
