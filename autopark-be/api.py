# import pandas as pd
# import numpy as np

from flask import Flask, json_available, jsonify
from flask_cors import CORS, cross_origin
from flask import request
# import io
# from PIL import Image
import base64
import json
from datetime import datetime


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
    # print(encoded)

    num_plate=get_num_plate(content)

    checkin_record=get_checkin_record(num_plate)

    if checkin_record is None:
        return {
            "startTimer": True,
            "startTime": get_current_time()
        }

    response =	{
        "startTime": "09:30",
        "finishTime": "10:15",
        "totalTime": "45m",
        "amount": "$8.82",
        "image_b64": encoded,
        "numberPlate": "AWK477"
    }

    return response

def write_json(data):
    with open('visits.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def get_checkin_record(num_plate):
    with open('visits.json') as json_file:
        data = json.load(json_file)
        visits=data['visits']

        checkin_records=list(filter(lambda visit:is_checkin_record(visit,num_plate), visits))

        if not checkin_records:
            data['visits'].append({
                "startTime": get_current_time(),
                "numberPlate": num_plate
            })

            write_json(data)
            return None

        return checkin_records[0]

def is_checkin_record(visit, num_plate):
    if 'finishTime' in visit:
        # isc= visit['finishTime'] is None and visit['numberPlate'] == num_plate
        # print(isc)
        return False

    return True

def get_num_plate(content):
    return 'AWK477'


def get_current_time():
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H:%M")
    return dt_string

app.run()
