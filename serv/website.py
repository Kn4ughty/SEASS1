from flask import Flask
import logging

logging.basicConfig(encoding="utf-8", level=logging.INFO)

api = Flask(__name__)


def makeList(scores):
    api.logger.info("Making list")

    length: int = 10
    out = []
    sorted_scores = sorted(scores, key=lambda x: float(x["score"]), reverse=True)
    trimed = sorted_scores[:length]

    for element in trimed:
        a = []
        a.append(element["name"])
        a.append(element["score"])
        a.append(element["worstScore"])
        out.append(a)

    return out
