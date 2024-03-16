from flask import Flask
from flask import request
import json
import os
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
        # print(element)
        # print(type(element))

        a = []
        a.append(element["name"])
        a.append(element["score"])
        out.append(a)

    # trimed = f"{trimed['name']:<} {trimed['scores']:>10}"

    # out = trimed

    # print(out)
    return out