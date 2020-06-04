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

#TODO - Model prediction function
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
        "image_b64": encoded
    }

    return response

def get_image_with_bb(image):
    imgdata = base64.b64decode(str(image))

    print(imgdata)
    image = Image.open(io.BytesIO(imgdata))

    return image

    # BytesIO is an in-memory file abstraction so we don't have
    # to write any actual files to disk
    f = io.BytesIO()
    image_stream=Image.open(image.stream)
    image_stream.save(f,"PNG")
    image_png_bytes = f.getvalue()

    image_png_b64 = b64encode(image_png_bytes).decode()
    # remove newlines
    image_png_b64 = image_png_b64.replace('\n', '')
    image_data_url = 'data:image/png;base64,' + image_png_b64

    return image_data_url

app.run()
