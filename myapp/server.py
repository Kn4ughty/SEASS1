from flask import Flask
from flask import request
import json
import pygame as pg
import os

api = Flask(__name__)


stupidtempdata = [{"name": "bob", "score": "312.5000", "UUID": "yadayada"},
          {"name": "jane", "score": "250.1235", "UUID": "woea"}]


prefPath = pg.system.get_pref_path("naught", "MOONLANDER")
databasePath = prefPath + "server/database.json"

if not os.path.exists(prefPath + "server/database.json"):
    #os.makedirs(prefPath + "server")
    print("grraaa")
    thing = open(databasePath, "w")
    json.dump(stupidtempdata, thing)
    thing.close()


@api.route('/scores', methods=['GET'])
def get_scores():
    print("gettingscores")
    with open(databasePath, "r") as database_file:
        scores = json.load(database_file)


    sorted_scores = sorted(scores, key=lambda x: float(x['score']), reverse=True)

    return json.dumps(sorted_scores)


@api.route('/scoresPost', methods=['POST'])
def post_scores():

    with open(databasePath, "r") as database_file:
        scores = json.load(database_file)

    request_data = request.get_json()

    #if len(scores) >= 1000:
    #    return json.dumps({"error": "Database full. Cannot add more entries."}), 400

    print(request_data)
    name = request_data['name']
    name = (name[:75] + '..') if len(name) > 75 else name
    score = request_data['score']

    score = str(round(float(score), 4))
    score = (score[:75]) if len(score) > 75 else score


    uuid = request_data['UUID']
    score = (score[:75] + '..') if len(score) > 75 else score

    print(f"{name} {score} {uuid}")


    scores.append({"name": name, "score": score, "UUID": uuid})

    scores = scores[:100]

    # Writing updated scores to database file
    with open(databasePath, "w") as database_file:
        json.dump(scores, database_file)

    return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run()