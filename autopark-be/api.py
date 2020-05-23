import pandas as pd 
import numpy as np 

from flask import Flask, json_available, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello_world():
    response = { 'Status': "API is up and running!" }
    return jsonify(response),200

#TODO - data pre-processing function
def preprocess():
    print("1")

#TODO - Model prediction function    
@app.route('/predict')
def predict():
    print("2")


app.run()
