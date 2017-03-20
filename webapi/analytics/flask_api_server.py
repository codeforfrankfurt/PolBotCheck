from flask import Flask
import db
import json


######################### FLASK APP
app = Flask(__name__)


@app.route("/pbc")
def index():
    """
    You know this is just the index because it is hard to visualize emptiness
    """
    return "PolBotCheck smart API v0.0.1"

@app.route("/pbc/user/<user_id>")
def user_info(user_id=None):
    """
    """
    if user_id is None:
        return "User not provided"

    user_data = db.getUser(user_id)
    if user_data is None:
        return "User lost in the dark forest - make a donation for us to find this user."

    TMP_namespace = "followerOfmalechanissen"

    json_output = {
        "content": "MEMBER", 
        "member":{
            "name" : user_data[TMP_namespace]["screen_name"],
            "pictureURL": user_data[TMP_namespace]["profile_image_url"],
            "party": "CDU",
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
        "botness": user_data["botness"]
    }

    return json.dumps(json_output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6755)
