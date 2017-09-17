from flask import Flask, request, jsonify
from flask_cors import CORS

#import db
import os
import json


######################### FLASK APP
app = Flask(__name__)
CORS(app)


@app.route("/pbc")
def index():
    """
    You know this is just the index because it is hard to visualize emptiness
    """
    return "PolBotCheck smart API v0.0.1"

def get_candidate_json(slug):
    candidates_path = os.path.join(os.path.realpath(os.getcwd()), '../web/public/candidates.json')

    with open(candidates_path) as file_stream:
        json_data = json.load(file_stream)

    for candidate in json_data:
        if candidate['slug'] == slug:
            return candidate

    return None

def get_full_name(json_data):
    name = None if not json_data else json_data['name']
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


@app.route("/pbc/user/<user_id>")
def user_info(user_id=None):
    """
    """
    if user_id is None:
        return "User not provided"

    candidate_json = get_candidate_json(user_id)
    full_name = get_full_name(candidate_json)

    #user_data = db.getUser('malechanissen')
    #if user_data is None:
    #    return "User lost in the dark forest - make a donation for us to find this user."

    json_output = {
        "content": "MEMBER", 
        "member":{
            "name" : full_name,
            "pictureURL": '',
            "party": candidate_json["election"]["party"],
        },
        "wordCluster":{},
        "followers": {
              "numFollowers": 16,
              "numHumans": 4,
              "numBots": 12
            },
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
        "botness": {}# if not user_data else user_data["botness"]
    }

    return jsonify(json_output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6755)
