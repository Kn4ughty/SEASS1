from flask import Flask
from flask import request
import json
import os
import logging

api = Flask(__name__)

def makeList(scores):
    print(len(scores))
    
    out = scores

    return out
