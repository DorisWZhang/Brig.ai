from flask import Flask, request, jsonify
import pickle
import pandas as pd

from flask_cors import CORS
import os
import numpy
import json

app = Flask(__name__)
CORS(app)

# Load pre-trained models and scaler
with open('./models/GradientBoosting_model.pkl', 'rb') as file:
    clf = pickle.load(file)

with open('./models/KMeans_model.pkl', 'rb') as file:
    kmeans = pickle.load(file)

with open('./models/scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "./models/endo_LR.pkl")
severity_model = pickle.load(open(MODEL_PATH, 'rb'))

MODEL_PATH = os.path.join(APP_ROOT, "./models/endo_LR_cluster.pkl")
cluster_model = pickle.load(open(MODEL_PATH, 'rb'))

ENDO_CLUSTER_JSON = {
    "Menstrual pain (Dysmenorrhea)": None,
    "Painful / Burning pain during sex (Dyspareunia)": None,
    "Irregular / Missed period": None,
    "Cramping": None,
    "Abdominal pain / pressure": None,
    "Painful bowel movements": None,
    "Infertility": None,
    "Painful cramps during period": None,
    "Constipation / Chronic constipation": None,
    "Vomiting / constant vomiting": None,
    "Fatigue / Chronic fatigue": None,
    "Painful ovulation": None,
    "Extreme / Severe pain": None,
    "Bleeding": None,
    "Fertility Issues": None,
    "Ovarian cysts": None,
    "Constant bleeding": None,
    "IBS-like symptoms": None,
    "Vaginal Pain/Pressure": None,
    "Bowel pain": None,
    "Cysts (unspecified)": None,
    "Malaise / Sickness": None,
    "Abnormal uterine bleeding": None,
    "Fever": None,
    "Hormonal problems": None,
    "Bloating": None,
    "Feeling sick": None,
    "Loss of appetite": None,
}

ENDO_PREDICT_JSON = {
    "Lower back pain": None,
    "Fever": None,
    "Cysts (unspecified)": None,
    "Bowel pain": None,
    "Fatigue / Chronic fatigue": None,
    "Irregular / Missed periods": None,
    "Painful / Burning pain during sex (Dyspareunia)": None,
    "Painful ovulation": None,
    "Menstrual pain (Dysmenorrhea)": None,
    "Fertility Issues": None,
    "Loss of appetite": None,
    "Malaise / Sickness": None,
    "Hormonal problems": None,
    "Bloating": None,
    "Headaches": None,
    "Extreme / Severe pain": None,
    "Ovarian cysts": None,
    "Vomiting / constant vomiting": None,
    "Bleeding": None,
    "Painful bowel movements": None,
    "Constant bleeding": None,
    "Painful cramps during period": None,
    "Infertility": None,
    "IBS-like symptoms": None,
    "Pelvic pain": None,
    "Abnormal uterine bleeding": None,
    "Constipation / Chronic constipation": None
}

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
PCOS_PREDICT_JSON = PCOS_PREDICT_JSON.copy()


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
    response_data = {'Updated cluster json': ENDO_CLUSTER_JSON,
                     'Updated predict json': ENDO_PREDICT_JSON}

    print(json.dumps(response_data, indent=2))
    return jsonify(response_data)


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
    cluster = int(numpy.argmax(cluster[0]))

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
