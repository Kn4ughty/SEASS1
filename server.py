from flask import Flask
import json

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

scores = [{"name": "bob", "score": "20.5000", "UUID": "yadayada"},
          {"name": "jane", "score": "250.1235", "UUID": "woea"}]

api = Flask(__name__)

@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

@api.route('/scores', methods=['GET'])
def get_scores():

   return json.dumps(scores)


if __name__ == '__main__':
    api.run()