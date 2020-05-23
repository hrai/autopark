import pandas as pd
import numpy as np

from flask import Flask, json_available, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors= CORS(app)
app.config["DEBUG"] = True
app.config["CORS_HEADERS"] = 'Content-Type'

@app.route('/', methods=['GET'])
@cross_origin()
def hello_world():
    response = { 'Status': "API is up and running!" }
    return jsonify(response),200

#TODO - data pre-processing function
def preprocess():
    print("1")

#TODO - Model prediction function
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict(data):
    # print(data)
    return 'predicted',200


app.run()
