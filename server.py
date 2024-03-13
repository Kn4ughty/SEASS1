from flask import Flask
from flask import request
import json
import atexit

api = Flask(__name__)

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

scores = [{"name": "bob", "score": "312.5000", "UUID": "yadayada"},
          {"name": "jane", "score": "250.1235", "UUID": "woea"}]


database = open("database.txt", "w") # lmao i find database.txt funny

atexit.register(database.close) # little silly. Wont be a problem if it never crashes :)



@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

@api.route('/scores', methods=['GET'])
def get_scores():

   return json.dumps(scores)

@api.route('/scoresGet', methods=['POST'])
def post_scores():
    #data = request.form
    #print(data)
    #print(request)
    #print("here is the name")
    #print(request.form.get('name'))
    request_data = request.get_json()
    print(request_data)
    name = request_data['name']
    score = request_data['score']
    uuid = request_data['UUID']

    


    return json.dumps({"success": True}), 201


if __name__ == '__main__':
    api.run()