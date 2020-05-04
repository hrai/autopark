import pandas as pd 
import numpy as np 
import tensorflow

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


#TODO - data pre-processing function
def preprocess():
    print("1")


#TODO - Model prediction function    
@app.route('/predict')
def predict():
    print("2")