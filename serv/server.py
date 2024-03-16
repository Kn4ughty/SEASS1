from flask import Flask, request, render_template, Response
import json
import pygame as pg
import os
import logging

import website


api = Flask(__name__)




stupidtempdata = [{"name": "bob", "score": "312.5000", "UUID": "yadayada"},
          {"name": "jane", "score": "250.1235", "UUID": "woea"}]


prefPath = pg.system.get_pref_path("naught", "MOONLANDER")
databasePath = os.path.join(prefPath + "server/database.json")
print(databasePath)

logging.basicConfig(filename=f"{prefPath}server/latest.log", encoding='utf-8', level=logging.INFO)



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






@api.route('/', methods=['GET'])
def serveMain():
    #return website.makeList()
    return render_template("index.html", list=website.makeList(get_db()))

@api.route('/mycss.css', methods=['GET'])
def serveCSS():
    #return website.makeList()
    with open("serv/templates/mycss.css", "r") as cssFile:
        css = cssFile.read()
    return Response(css, mimetype='text/css') # Why do i have to specify mimetype


def get_db():
    logging.info("getting the database")
    with open(databasePath, "r") as database_file:
        scores = json.load(database_file)

    return scores

@api.route('/scores', methods=['GET'])
def get_scores():

    scores = get_db()

    sorted_scores = sorted(scores, key=lambda x: float(x['score']), reverse=True)

    out = []

    for element in sorted_scores:
        element.pop("UUID") # lets see if this breaks things 
        out.append(element)

    return json.dumps(sorted_scores)


@api.route('/scoresPost', methods=['POST'])
def post_scores():

    with open(databasePath, "r") as database_file:
        scores = json.load(database_file)

    request_data = request.get_json()

    #if len(scores) >= 1000:
    #    return json.dumps({"error": "Database full. Cannot add more entries."}), 400

    name = str(request_data['name'][:75])  # Truncate name if it's longer than 75 characters
    score = str(round(float(request_data['score']), 4))[:75]  # Convert score to string and truncate if longer than 75 characters
    uuid = str(request_data['UUID'])

    formatedNew = {"name": name, "score": score, "UUID": uuid}

    dupli = False

    for i in range(len(scores)):
        if scores[i]['UUID'] == uuid:
            logging.info(f"Found duplicate UUDI in entry {i}")
            if float(scores[i]['score']) >= float(score): # if old score is more than new score
                logging.info(f"Old score was higher than the new score\n Old score: {scores[i]['score']:<10} new score: {score:<10}")
                return json.dumps({"error": "An entry with this UUID already exists in the database and it was lower than previous score."}), 409
            else:
                # the score is better than existing one of saeme UUID
                scores[i] = formatedNew
                dupli = True

    if len(scores) < 1000 or float(score) > float(scores[-1]['score']):
        if not dupli:
            scores.append(formatedNew)
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