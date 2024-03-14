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
    os.mkdir(prefPath + "server/")
    thing = open(databasePath, "x")
    thing.close()

if os.stat(databasePath).st_size == 0:
    print("writing stupid data")
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

    name = request_data['name'][:75]  # Truncate name if it's longer than 75 characters
    score = str(round(float(request_data['score']), 4))[:75]  # Convert score to string and truncate if longer than 75 characters
    uuid = request_data['UUID']

    for entry in scores:
        if entry['UUID'] == uuid:
            return json.dumps({"error": "An entry with this UUID already exists in the database."}), 409

    print(scores)
    print(scores[-1])

    if len(scores) < 1000 or float(score) > float(scores[-1]['score']):
        scores.append({"name": name, "score": score, "UUID": uuid})
        # Sort the scores
        sortedDB = sorted(scores, key=lambda x: float(x['score']), reverse=True)
        # Truncate to keep only the top 1000 scores
        sortedDB = sortedDB[:1000]
        # Writing updated scores to database file
        with open(databasePath, "w") as database_file:
            json.dump(sortedDB, database_file)
        return json.dumps({"success": True}), 201
    else:
        return json.dumps({"error": "Score is not higher than the lowest score in the database."}), 400

if __name__ == '__main__':
    api.run()