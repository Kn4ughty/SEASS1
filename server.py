from flask import Flask
from flask import request
import json

api = Flask(__name__)


scores = [{"name": "bob", "score": "312.5000", "UUID": "yadayada"},
          {"name": "jane", "score": "250.1235", "UUID": "woea"}]


with open("database.txt", "w") as database_file:
    json.dump(scores, database_file)



@api.route('/scores', methods=['GET'])
def get_scores():
    with open("database.txt", "r") as database_file:
        scores = json.load(database_file)

    sorted_scores = sorted(scores, key=lambda x: float(x['score']), reverse=True)

    return json.dumps(sorted_scores)


@api.route('/scoresPost', methods=['POST'])
def post_scores():

    with open("database.txt", "r") as database_file:
        scores = json.load(database_file)

    request_data = request.get_json()

    #if len(scores) >= 1000:
    #    return json.dumps({"error": "Database full. Cannot add more entries."}), 400

    print(request_data)
    name = request_data['name']
    name = (name[:75] + '..') if len(name) > 75 else name
    score = request_data['score']
    score = (score[:75] + '..') if len(score) > 75 else score
    uuid = request_data['UUID']
    score = (score[:75] + '..') if len(score) > 75 else score

    print(f"{name} {score} {uuid}")


    scores.append({"name": name, "score": score, "UUID": uuid})

    scores = scores[:100]

    # Writing updated scores to database file
    with open("database.txt", "w") as database_file:
        json.dump(scores, database_file)

    return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run()