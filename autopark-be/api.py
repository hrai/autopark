import pandas as pd
import numpy as np

from flask import Flask, json_available, jsonify
from flask_cors import CORS, cross_origin
from flask import request

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
def predict():
    # print(data)
    formData=request.form
    filename=formData['filename']

    response =	{
        "startTime": "09:30",
        "finishTime": "10:15",
        "totalTime": "45m",
        "amount": "$8.82"
    }

    return response

app.run()
