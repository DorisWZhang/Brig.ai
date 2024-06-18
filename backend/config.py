import pickle
from flask import Flask, render_template
from flask_cors import CORS
import pandas as pd
from flask import request, jsonify
import os
import numpy

from sklearn.linear_model import LogisticRegression
app = Flask(__name__)
CORS(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "./models/endo_LR.pkl")
severity_model = pickle.load(open(MODEL_PATH, 'rb'))

MODEL_PATH = os.path.join(APP_ROOT, "./models/endo_LR_cluster.pkl")
cluster_model = pickle.load(open(MODEL_PATH, 'rb'))


@app.route('/endoseverity', methods=['POST'])
def model_predict():
    data = request.get_json()  # Get the JSON data from the request
    features = [int(x) for x in data.values()]
    df = pd.DataFrame([features], columns=data.keys())
    severity_prediction = severity_model.predict_proba(df)
    severity_prediction = severity_prediction[0][1]

    return jsonify({'severity': severity_prediction})


@app.route('/endocluster', methods=['POST'])
def model_cluster():
    data = request.get_json()  # Get the JSON data from the request
    features = [[int(x) for x in data.values()]]
    cluster = cluster_model.predict_proba(features)
    cluster = int(numpy.argmax(cluster[0]))
    return jsonify({'cluster': cluster})


if __name__ == "__main__":
    app.run(debug=True)

# render_template allows you to return an html file instead of a
# the html code as a string
