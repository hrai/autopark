import tensorflow as tf
from tensorflow.keras.applications.xception import Xception, preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
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
        # extract image data to numpy array
        image_path = os.path.join(directory, input_image)
        img = image.load_img(image_path, target_size=target_size)
        img_arr = image.img_to_array(img)
        img_arr = preprocess_input(img_arr) # Xception preprocessing

        return img_arr


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    # fetch payload from response, including input image
    formData=request.form
    filename='num_plate'
    image=request.files[filename]
    
    # pre-process input image
    processed_image = preprocess(image)

    # generate prediction on imput image, get bounding box
    y_pred = model.predict(X_test) 
    get_bbox(y_pred[0])

    img = image.array_to_img(X_test[index])
    ax[i, j].imshow(img)
    ax[i, j].axis("off")

    # predicted coordinates
    xmin_p, ymin_p, xmax_p, ymax_p = y_pred
    width_p = xmax_p - xmin_p
    height_p = ymax_p - ymin_p

    # draw bounding boxes; lime = ground truth, red = predicted
    rect_p = patches.Rectangle((xmin_p, ymin_p), width_p, height_p, linewidth=2, edgecolor="red", facecolor="none")
    ax[i, j].add_patch(rect_p)
    
    # save annotated figure as image
    plt.savefig('output.png')

    # convert output image to jpg
    Image.open('output.png').save('output.jpg', 'JPEG')


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
