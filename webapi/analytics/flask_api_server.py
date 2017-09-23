import os

if not os.environ.get('FLASK_ENV') == 'production':
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)

from flask import Flask, jsonify
from flask_cors import CORS

######################### FLASK APP
app = Flask(__name__)
CORS(app)

print("Value of WEB_CONCURRENCY is %s" % os.environ.get('WEB_CONCURRENCY'))
if int(os.environ.get('WEB_CONCURRENCY')) > 1:
    # sleep for a random interval to avoid all workers hitting
    # the database multiple times on bootup
    from random import randint
    from time import sleep
    interval = randint(4,20)
    print("Sleep for %d seconds to avoid too many concurrent db hits" % interval)
    sleep(interval)
import db


######################### ACTIONS
@app.route("/pbc")
def index():
    """
    Return organizational entities like Landesliste Hessen and the hessian election districts
    as well as the candidates in them
    """
    groupings = []
    candidates_by_district = db.get_candidates_grouped_by_district()
    for group in candidates_by_district:
        print(group)
        groupings.append(group)
    return jsonify({'candidates_grouped_by_district': groupings})


@app.route("/pbc/districts")
def districts():
    """
    Return organizational entities like Landesliste Hessen and the hessian election districts
    """
    districts = []
    for district in db.get_districts():
        districts.append({'id': int(district['_key']), 'name': district['name']})
    return jsonify({'districts': districts})


@app.route("/pbc/districts/<slug>")
def show_district(slug=None):
    """
    Return one organizational entity like Landesliste Hessen or a hessian election district
    as well as the candidates in them
    """
    groupings = []
    candidates = db.get_candidates_by_district(slug)
    for group in candidates_in_district:
        print(group)
        groupings.append(group)
    return jsonify({'district': groupings})


@app.route("/pbc/parties/<slug>")
def show_party(slug=None):
    """
    Return organizational entities like Landesliste Hessen and the hessian election districts
    as well as the candidates in them
    """
    members = []
    candidates_by_party = db.get_candidates_by_party(slug)
    for candidate in candidates_by_party:
        print(candidate)
        members.append(candidate)
    return jsonify({'candidates_by_party': members})


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


@app.route("/pbc/users/<slug>")
def show_candidate(slug=None):
    """
    """
    if slug is None:
        return "Candidate not provided"

    candidate = db.get_candidate(slug)
    if candidate is None:
        return "Candidate not found"

    full_name = get_full_name(candidate['name'])

    twitter_user = db.getUser(candidate.get('twitter_handle'))
    twitter_data = None
    followers = {"numFollowers": None}
    word_cluster = {'topics': []}
    if twitter_user:
        twitter_data = {"profile_url": twitter_user["twitter"]["profile_image_url_https"]}
        followers["numFollowers"] = twitter_user["twitter"]["followers_count"]
        follower_stats = db.getFollowerStats(candidate['twitter_handle'])
        followers.update(follower_stats)
        word_frequencies = twitter_user.get('word_frequencies')
        if word_frequencies:
            word_cluster = word_frequencies

    json_output = {
        "content": "MEMBER", 
        "member": {
            "name": full_name,
            "party": candidate["election"]["party"],
            "twitter_handle": candidate.get('twitter_handle'),
            "facts" : candidate["facts"],
            "links" : candidate["links"],
            "photos" : candidate["photos"]
        },
        "twitter": twitter_data,
        "wordCluster": word_cluster,
        "followers": followers,
        "retweets": {
              "numRetweets": None,
              "numHumans": None,
              "numBots": None
        },
        "retweeters": {
              "numRetweeters": None,
              "numHumans": None,
              "numBots": None
        },
        "election": candidate['election'],
        "botness": twitter_user["botness"] if twitter_user and "botness" in twitter_user else {}
    }

    return jsonify(json_output)


if __name__ == "__main__":
    port = os.environ.get('PORT') or 6755
    app.run(host="0.0.0.0", port=port)
