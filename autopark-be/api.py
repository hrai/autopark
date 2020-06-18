import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import cv2
from tensorflow.keras.applications.xception import Xception, preprocess_input
from tensorflow.keras.preprocessing import image as k_image
from tensorflow.keras.models import load_model
from tensorflow import keras
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


def mean_iou(a, b):
    """ Given two arrays `a` and `b` where each row contains a bounding
        box defined as a list of four numbers:
            [x1,y1,x2,y2]
        where:
            x1,y1 represent the upper left corner
            x2,y2 represent the lower right corner
        It returns the mean of the Intersect of Union scores for each corresponding
        pair of boxes.

    Args:
        a:          (numpy array) each row containing [x1,y1,x2,y2] coordinates
        b:          (numpy array) each row containing [x1,y1,x2,y2] coordinates

    Returns:
        (float) The mean of the Intersect of Union scores for each pair of bounding
        boxes.
    """
    epsilon = keras.backend.epsilon()
    
    # COORDINATES OF THE INTERSECTION BOXES
    x1 = keras.backend.max([a[:, 0], b[:, 0]], axis=0)
    y1 = keras.backend.max([a[:, 1], b[:, 1]], axis=0)
    x2 = keras.backend.min([a[:, 2], b[:, 2]], axis=0)
    y2 = keras.backend.min([a[:, 3], b[:, 3]], axis=0)

    # AREAS OF OVERLAP - Area where the boxes intersect
    width = (x2 - x1)
    height = (y2 - y1)

    # handle case where there is NO overlap
    width = keras.backend.maximum(width, 0)
    height = keras.backend.maximum(height, 0)

    area_overlap = width * height

    # COMBINED AREAS
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    area_combined = area_a + area_b - area_overlap

    # RATIO OF AREA OF OVERLAP OVER COMBINED AREA
    iou = area_overlap / (area_combined + epsilon)
    
    # Mean IoU 
    iou_mean = keras.backend.mean(iou)
    
    return iou_mean


# Serve tf model globally to reduce memory load & ensure availability
dependencies = {
    'mean_iou': mean_iou
}

loaded_plate_model = tf.keras.models.load_model('models/model.59-mIoU0.8160.h5', custom_objects=dependencies)
loaded_char_model = tf.keras.models.load_model('models/model.10-acc1.0000.h5')


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

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

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
    cropped_plate = k_image.img_to_array(img.crop((xmin, ymin, xmax, ymax)))

    # save annotated figure as image
    filename=randomString()
    filepath = "output_" + filename + ".jpg"
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
    y_pred = loaded_plate_model.predict(processed_image)
    y_pred = y_pred[0] * 512 # de-normalises bounding box predictions

    # draw bbox on image and save; get filepath and cropped plate image
    img_path, cropped_plate = save_patched_img(processed_image[0], y_pred)

    # convert output image to jpg
    # Image.open('output.png').save('output.jpg', 'JPEG')
    Image.open(img_path).save('output.png')

    # content = image.read()

    encoded = base64.b64encode('output.png')

    # Get character array
    char_arr = get_localized_images(cropped_plate)

    # Parsed number plate from OCR model
    num_plate=get_num_plate(char_arr)
    print(num_plate)

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
        "numberPlate": num_plate
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

# Get character classification prediction for a single image
def cnnCharRecognition(img):
    image = img / 255.0
    image = np.reshape(image, (1,71,71,3))
    new_predictions = loaded_char_model.predict(image)
    char = np.argmax(new_predictions)
    
    return dictionary[char]

# Return estimated number plate from model
def get_num_plate(char_array):
   
    for img in char_array:
        img = array_to_img(img)
        img = img.convert('LA')
        img = img.resize((71,71)) 
        img = np.asarray(img, dtype='float32')
        pred = cnnCharRecognition(img)
        numberplate.append(pred)

        return ''.join(numberplate)
       

# Get localized number plate characters in array form to pass into classificatio model
def get_localized_images(cropped_plate):
    print(cropped_plate.shape)
   
   
   
    # Loop through each image, apply pre-processing & localize onto each character
    gray = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2GRAY)
    
    thresh_inv = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,39,1)
    edges = auto_canny(thresh_inv)
    ctrs, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    img_area = img.shape[0]*img.shape[1]

    # Get bounding box co-ordinates for image cropping
    for i, ctr in enumerate(sorted_ctrs):
        x, y, w, h = cv2.boundingRect(ctr)
        roi_area = w*h
        roi_ratio = roi_area/img_area

        if((roi_ratio >= 0.04) and (roi_ratio < 0.16)):
                if ((h>0.9*w) and (2.8*w>=h)):
                    cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255), 1)
                    bounding_boxes.append((x,y,w,h))
                    counter += 1

    # Crop bounding boxes and save into new dir
    count = 0
    char_array = []
    for box in bounding_boxes:
            x,y,w,h = box
            ROI = img[y:y+h, x:x+w]
            char_array.append(ROI)
            # cv2.imwrite("/images/char_{}.png".format(str(count)), ROI)
            count += 1

    return char_array


def get_current_time():
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H:%M")
    return dt_string


app.run()
