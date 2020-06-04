import pandas as pd
import numpy as np

from flask import Flask, json_available, jsonify
from flask_cors import CORS, cross_origin
from flask import request
import io
import base64
from PIL import Image

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

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    formData=request.form
    filename='num_plate'
    image=request.files[filename]
    content = image.read()

    encoded = base64.b64encode(content)
    print(encoded)

    response =	{
        "startTime": "09:30",
        "finishTime": "10:15",
        "totalTime": "45m",
        "amount": "$8.82",
        "image_b64": encoded,
        "numberPlate": "AWK477"
    }

    return response

