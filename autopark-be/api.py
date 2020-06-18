import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
from tensorflow.keras.applications.xception import Xception, preprocess_input
from tensorflow.keras.preprocessing import k_image
from tensorflow.keras.models import load_model
from PIL import Image
from flask import Flask, json_available, jsonify
from flask_cors import CORS, cross_origin
from flask import request
from datetime import datetime

import base64
import json

app = Flask(__name__)
cors= CORS(app)
app.config["DEBUG"] = True
app.config["CORS_HEADERS"] = 'Content-Type'


# Serve tf model globally to reduce memory load & ensure availability
model = tf.keras.models.load_model('/models/production_model.h5')

@app.route('/', methods=['GET'])
@cross_origin()
def hello_world():
    response = { 'Status': "API is up and running!" }
    return jsonify(response),200


def preprocess(input_image):
    # load and resize the image
    img = Image.open(input_image)
    img = img.resize((512, 512))

    # extract image data to numpy array
    img_arr = k_image.img_to_array(img)
    img_arr = preprocess_input(img_arr) # Xception preprocessing

    # reshape array to include batch size (1 in this case) since model was trained on batches
    # e.g. [512, 512, 3] to [1, 512, 512, 3]
    img_arr = np.expand_dims(img_arr, axis=0)

    return img_arr


def save_patched_img(img, bbox):
    """ Saves images with bounding box drawn on it.
    Returns: (string) Filepath of saved image """

    # plot image
    fig, ax = plt.subplots(1, figsize=(10, 10))

    img = k_image.array_to_img(img)
    ax.imshow(img)
    ax.axis("off")

    # predicted coordinates
    xmin, ymin, xmax, ymax = bbox
    width = xmax - xmin
    height = ymax - ymin

    # draw predicted bounding box on image
    rect = patches.Rectangle((xmin, ymin), width, height, linewidth=2, edgecolor="red", facecolor="none")
    ax.add_patch(rect)

    # crop image to plate and save
    cropped_plate = img.crop((xmin, ymin, xmax, ymax))
    cropped_plate.save("cropped_plate.jpg")
    
    # save annotated figure as image
    filepath = "output.png"
    fig.savefig(filepath)

    return filepath, cropped_plate


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    # fetch payload from response, including input image
    formData = request.form
    filename = 'num_plate'
    image = request.files[filename]
    
    # pre-process input image
    processed_image = preprocess(image)

    # generate prediction on input image, get bounding box
    y_pred = model.predict(processed_image)
    y_pred = y_pred[0] * 512 # de-normalises bounding box predictions

    # draw bbox on image and save; get filepath and cropped plate image
    img_path, cropped_plate = save_patched_img(processed_image[0], y_pred)

    # convert output image to jpg
    # Image.open('output.png').save('output.jpg', 'JPEG')
    Image.open(img_path).save('output.jpg', 'JPEG')


    # content = image.read()

    encoded = base64.b64encode('output.png')

    # Parsed number plate from OCR model
    num_plate=get_num_plate(content)

    checkin_record=get_checkin_record(num_plate)

    # Check if recognised vehicle has checked in before, otherwise start a new parking session
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
