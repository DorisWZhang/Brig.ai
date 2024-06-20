from flask import Flask, request, jsonify
import pickle
import pandas as pd

from flask_cors import CORS
import os
import numpy as np
import json

app = Flask(__name__)
CORS(app)

# Load pre-trained models and scaler
with open('./models/GradientBoosting_model.pkl', 'rb') as file:
    clf = pickle.load(file)

with open('./models/AdaBoost_model.pkl', 'rb') as file:
    abc = pickle.load(file)

with open('./models/logistic_regression_model.pkl', 'rb') as file:
    logistic_regression = pickle.load(file)

with open('./models/KMeans_model.pkl', 'rb') as file:
    kmeans = pickle.load(file)

with open('./models/scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "./models/endo_LR.pkl")
severity_model = pickle.load(open(MODEL_PATH, 'rb'))

MODEL_PATH = os.path.join(APP_ROOT, "./models/endo_LR_cluster.pkl")
cluster_model = pickle.load(open(MODEL_PATH, 'rb'))

ENDO_CLUSTER_JSON = {"Menstrual pain (Dysmenorrhea)": 0.0, "Painful / Burning pain during sex (Dyspareunia)": 0.0, "Pelvic pain": 0.0, "Irregular / Missed periods": 0.0, "Cramping": 0.0, "Abdominal pain / pressure": 0.0, "Painful bowel movements": 0.0, "Infertility": 0.0, "Painful cramps during period": 0.0, "Constipation / Chronic constipation": 0.0, "Vomiting / constant vomiting": 0.0, "Fatigue / Chronic fatigue": 0.0, "Painful ovulation": 0.0,
                     "Extreme / Severe pain": 0.0, "Bleeding": 0.0, "Fertility Issues": 0.0, "Ovarian cysts": 0.0, "Constant bleeding": 0.0, "IBS-like symptoms": 0.0, "Vaginal Pain/Pressure": 0.0, "Bowel pain": 0.0, "Cysts (unspecified)": 0.0, "Malaise / Sickness": 0.0, "Abnormal uterine bleeding": 0.0, "Fever": 0.0, "Hormonal problems": 0.0, "Bloating": 0.0, "Feeling sick": 0.0, "Loss of appetite": 0.0, "Diagnosed with Endometriosis": 0.0}

ENDO_PREDICT_JSON = {"Menstrual pain (Dysmenorrhea)": 0, "Painful / Burning pain during sex (Dyspareunia)": 0, "Pelvic pain": 0, "Irregular / Missed periods": 0, "Painful bowel movements": 0, "Infertility": 0, "Painful cramps during period": 0, "Constipation / Chronic constipation": 0, "Vomiting / constant vomiting": 0, "Fatigue / Chronic fatigue": 0, "Painful ovulation": 0,
                     "Extreme / Severe pain": 0, "Bleeding": 0, "Lower back pain": 0, "Fertility Issues": 0, "Ovarian cysts": 0, "Headaches": 0, "Constant bleeding": 0, "IBS-like symptoms": 0, "Bowel pain": 0, "Cysts (unspecified)": 0, "Malaise / Sickness": 0, "Abnormal uterine bleeding": 0, "Fever": 0, "Hormonal problems": 0, "Bloating": 0, "Loss of appetite": 0}

PCOS_PREDICT_JSON = {
    "Age (yrs)": None,
    "Weight (Kg)": None,
    "Height(Cm)": None,
    "Pulse rate(bpm)": None,
    "RR (breaths/min)": None,
    "Cycle(R/I)": None,
    "Cycle length(days)": None,
    "Marraige Status (Yrs)": None,
    "Pregnant(Y/N)": None,
    "No. of abortions": None,
    "Hip(inch)": None,
    "Waist(inch)": None,
    "Waist:Hip Ratio": None,
    "Weight gain(Y/N)": None,
    "hair growth(Y/N)": None,
    "Skin darkening (Y/N)": None,
    "Hair loss(Y/N)": None,
    "Pimples(Y/N)": None,
    "Fast food (Y/N)": None,
    "Reg.Exercise(Y/N)": None,
    "BP _Systolic (mmHg)": None,
    "BP _Diastolic (mmHg)": None
}

ENDO_PREDICT_JSON_NULL = ENDO_PREDICT_JSON.copy()
ENDO_CLUSTER_JSON_NULL = ENDO_CLUSTER_JSON.copy()
PCOS_PREDICT_JSON_NULL = PCOS_PREDICT_JSON.copy()


@app.route('/update', methods=['POST'])
def update():
    input_data = request.get_json()

    print("INPUT DATA")
    print(json.dumps(input_data, indent=2))

    for key in input_data:
        if key in ENDO_CLUSTER_JSON:
            ENDO_CLUSTER_JSON[key] = input_data[key]
        if key in ENDO_PREDICT_JSON:
            ENDO_PREDICT_JSON[key] = input_data[key]
        if key in PCOS_PREDICT_JSON:
            PCOS_PREDICT_JSON[key] = input_data[key]
    response_data = {'Updated cluster json': ENDO_CLUSTER_JSON,
                     'Updated predict json': ENDO_PREDICT_JSON,
                     'Updated pcos json': PCOS_PREDICT_JSON}

    print(json.dumps(response_data, indent=2))
    return jsonify(response_data)


@app.route('/submit', methods=['POST'])
def submit_final():
    global ENDO_CLUSTER_JSON, ENDO_PREDICT_JSON, PCOS_PREDICT_JSON
    input_data = request.get_json()  # Get the JSON data from the request

    for key in input_data:
        if key in ENDO_CLUSTER_JSON:
            ENDO_CLUSTER_JSON[key] = input_data[key]
        if key in ENDO_PREDICT_JSON:
            ENDO_PREDICT_JSON[key] = input_data[key]
        if key in PCOS_PREDICT_JSON:
            PCOS_PREDICT_JSON[key] = input_data[key]

    response_data = {'Updated cluster json': ENDO_CLUSTER_JSON.copy(),
                     'Updated predict json': ENDO_PREDICT_JSON.copy(),
                     'Updated pcos json': PCOS_PREDICT_JSON.copy()}

    # getting values relevant to making endo prediction
    endo_predict_features = [
        int(x) if x is not None else 0 for x in ENDO_PREDICT_JSON.values()]
    endo_predict_df = pd.DataFrame(
        [endo_predict_features], columns=ENDO_PREDICT_JSON.keys())
    endo_severity_prediction = severity_model.predict_proba(endo_predict_df)[
        0][1]
    ENDO_PREDICT_JSON = ENDO_PREDICT_JSON_NULL.copy()

    # endo cluster prediction
    endo_cluster_features = [
        [int(x) if x is not None else 0 for x in ENDO_CLUSTER_JSON.values()]]
    endo_cluster_prediction = int(
        np.argmax(cluster_model.predict_proba(endo_cluster_features)[0]))
    ENDO_CLUSTER_JSON = ENDO_CLUSTER_JSON_NULL.copy()

    # pcos prediction
    pcos_predict_features = [
        int(x) if x is not None else 0 for x in PCOS_PREDICT_JSON.values()]
    pcos_predict_df = pd.DataFrame(
        [pcos_predict_features], columns=PCOS_PREDICT_JSON.keys())
    pcos_predict_df.columns = pcos_predict_df.columns.str.strip()
    pcos_predict_df_scaled = scaler.transform(pcos_predict_df)
    pcos_severity_prediction = abc.predict_proba(
        pcos_predict_df_scaled)[0][1]
    
    # pcos cluster prediction
    logistic_predictions = logistic_regression.predict(pcos_predict_df_scaled).reshape(1, -1)
    pcos_cluster_predictions = kmeans.predict(logistic_predictions).tolist()

    response = {'endo_severity': endo_severity_prediction,
                'endo_cluster': endo_cluster_prediction,
                'pcos_severity': pcos_severity_prediction,
                'pcos_cluster': pcos_cluster_predictions[0]}
    print(response)

     # Ensuring all values in response are JSON serializable
    response = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in response.items()}
    
    return jsonify(response)


@app.route('/endoseverity', methods=['POST'])
def endo_predict():
    data = request.get_json()  # Get the JSON data from the request
    features = [int(x) for x in data.values()]
    df = pd.DataFrame([features], columns=data.keys())
    severity_prediction = severity_model.predict_proba(df)
    severity_prediction = severity_prediction[0][1]
    ENDO_PREDICT_JSON = ENDO_PREDICT_JSON_NULL
    return jsonify({'severity': severity_prediction, 'update prediction json': ENDO_PREDICT_JSON})


@app.route('/endocluster', methods=['POST'])
def endo_cluster():
    data = request.get_json()  # Get the JSON data from the request
    features = [[int(x) for x in data.values()]]
    cluster = cluster_model.predict_proba(features)
    cluster = int(np.argmax(cluster[0]))

    ENDO_CLUSTER_JSON = ENDO_CLUSTER_JSON_NULL
    return jsonify({'cluster': cluster, 'updated cluster json': ENDO_CLUSTER_JSON})


@app.route('/predictPCOS', methods=['POST'])
def predictPCOS():
    try:
        data = request.json
        if isinstance(data, list):  # Ensure that the input is a list
            df = pd.DataFrame(data)
            print("Received data:", df)  # Debug print

            # Ensure that column names are stripped of leading/trailing whitespace
            df.columns = df.columns.str.strip()

            # Standardize the features
            df_scaled = scaler.transform(df)

            # Predict probabilities using the classifier
            prediction_probabilities = clf.predict_proba(df_scaled)
            print("Prediction probabilities:",
                  prediction_probabilities)  # Debug print

            # Convert probabilities to a list of lists, negative, positive
            prediction_probabilities_list = prediction_probabilities.tolist()
            return jsonify({'prediction_probabilities': prediction_probabilities_list})
        else:
            return jsonify({'error': 'Input data should be a list of dictionaries'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictPCOScluster', methods=['POST'])
def predictPCOScluster():
    try:
        data = request.json
        if isinstance(data, list):  # Ensure that the input is a list
            df = pd.DataFrame(data)
            print("Received data:", df)  # Debug print

            # Ensure that column names are stripped of leading/trailing whitespace
            df.columns = df.columns.str.strip()

            # Standardize the features
            df_scaled = scaler.transform(df)

            # Print the scaled data for debugging
            print("Scaled data:", df_scaled)  # Debug print

            # Predict cluster using the kmeans model
            cluster_predictions = kmeans.predict(df_scaled)
            print("Cluster predictions:", cluster_predictions)  # Debug print

            # Calculate percentage of each cluster
            unique_clusters, cluster_counts = np.unique(
                cluster_predictions, return_counts=True)
            total_samples = len(cluster_predictions)
            cluster_percentages = {str(
                cluster): count / total_samples for cluster, count in zip(unique_clusters, cluster_counts)}

            return jsonify({'cluster_percentages': cluster_percentages})
        else:
            return jsonify({'error': 'Input data should be a list of dictionaries'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
