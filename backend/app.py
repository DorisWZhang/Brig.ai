import os
import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load models once on app startup
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

    with open(os.path.join(model_dir, 'GradientBoosting_model.pkl'), 'rb') as f:
        clf = pickle.load(f)
    with open(os.path.join(model_dir, 'AdaBoost_model.pkl'), 'rb') as f:
        abc = pickle.load(f)
    with open(os.path.join(model_dir, 'logistic_regression_model.pkl'), 'rb') as f:
        logistic_regression = pickle.load(f)
    with open(os.path.join(model_dir, 'KMeans_model.pkl'), 'rb') as f:
        kmeans = pickle.load(f)
    with open(os.path.join(model_dir, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(model_dir, 'endo_LR.pkl'), 'rb') as f:
        severity_model = pickle.load(f)
    with open(os.path.join(model_dir, 'endo_LR_cluster.pkl'), 'rb') as f:
        cluster_model = pickle.load(f)

    ENDO_PREDICT_KEYS = ["Menstrual pain (Dysmenorrhea)", "Painful / Burning pain during sex (Dyspareunia)", "Pelvic pain",
                         "Irregular / Missed periods", "Painful bowel movements", "Infertility", "Painful cramps during period",
                         "Constipation / Chronic constipation", "Vomiting / constant vomiting", "Fatigue / Chronic fatigue",
                         "Painful ovulation", "Extreme / Severe pain", "Bleeding", "Lower back pain", "Fertility Issues",
                         "Ovarian cysts", "Headaches", "Constant bleeding", "IBS-like symptoms", "Bowel pain", "Cysts (unspecified)",
                         "Malaise / Sickness", "Abnormal uterine bleeding", "Fever", "Hormonal problems", "Bloating", "Loss of appetite"]

    ENDO_CLUSTER_KEYS = ["Menstrual pain (Dysmenorrhea)", "Painful / Burning pain during sex (Dyspareunia)", "Pelvic pain",
                         "Irregular / Missed periods", "Cramping", "Abdominal pain / pressure", "Painful bowel movements", "Infertility",
                         "Painful cramps during period", "Constipation / Chronic constipation", "Vomiting / constant vomiting", "Fatigue / Chronic fatigue",
                         "Painful ovulation", "Extreme / Severe pain", "Bleeding", "Fertility Issues", "Ovarian cysts", "Constant bleeding",
                         "IBS-like symptoms", "Vaginal Pain/Pressure", "Bowel pain", "Cysts (unspecified)", "Malaise / Sickness",
                         "Abnormal uterine bleeding", "Fever", "Hormonal problems", "Bloating", "Feeling sick", "Loss of appetite", "Diagnosed with Endometriosis"]

    PCOS_PREDICT_KEYS = ["Age (yrs)", "Weight (Kg)", "Height(Cm)", "Pulse rate(bpm)", "RR (breaths/min)", "Cycle(R/I)", "Cycle length(days)",
                         "Marraige Status (Yrs)", "Pregnant(Y/N)", "No. of abortions", "Hip(inch)", "Waist(inch)", "Waist:Hip Ratio",
                         "Weight gain(Y/N)", "hair growth(Y/N)", "Skin darkening (Y/N)", "Hair loss(Y/N)", "Pimples(Y/N)", "Fast food (Y/N)",
                         "Reg.Exercise(Y/N)", "BP _Systolic (mmHg)", "BP _Diastolic (mmHg)"]

    # Helper function to initialize empty dict with keys set to 0 or None
    def empty_endo_predict_json():
        return {k: 0 for k in ENDO_PREDICT_KEYS}

    def empty_endo_cluster_json():
        return {k: 0 for k in ENDO_CLUSTER_KEYS}

    def empty_pcos_predict_json():
        return {k: None for k in PCOS_PREDICT_KEYS}

    @app.route('/submit', methods=['POST'])
    def submit_final():
        input_data = request.get_json()

        # Prepare fresh dicts per request
        endo_predict_json = empty_endo_predict_json()
        endo_cluster_json = empty_endo_cluster_json()
        pcos_predict_json = empty_pcos_predict_json()

        # Update with input data if keys exist
        for key in input_data:
            if key in endo_predict_json:
                endo_predict_json[key] = input_data[key]
            if key in endo_cluster_json:
                endo_cluster_json[key] = input_data[key]
            if key in pcos_predict_json:
                pcos_predict_json[key] = input_data[key]

        # Prepare data for prediction - use 0 or None defaults where needed
        endo_predict_features = [int(endo_predict_json.get(k, 0)) for k in ENDO_PREDICT_KEYS]
        endo_cluster_features = [[int(endo_cluster_json.get(k, 0)) for k in ENDO_CLUSTER_KEYS]]
        pcos_predict_features = [int(pcos_predict_json.get(k, 0)) if pcos_predict_json.get(k) is not None else 0 for k in PCOS_PREDICT_KEYS]

        # Predictions
        endo_severity = severity_model.predict_proba(pd.DataFrame([endo_predict_features], columns=ENDO_PREDICT_KEYS))[0][1]
        endo_cluster = int(np.argmax(cluster_model.predict_proba(endo_cluster_features)[0]))

        pcos_df = pd.DataFrame([pcos_predict_features], columns=PCOS_PREDICT_KEYS)
        pcos_df_scaled = scaler.transform(pcos_df)
        pcos_severity = abc.predict_proba(pcos_df_scaled)[0][1]

        logistic_preds = logistic_regression.predict(pcos_df_scaled).reshape(1, -1)
        pcos_cluster = kmeans.predict(logistic_preds)[0]

        response = {
            'endo_severity': float(endo_severity),
            'endo_cluster': int(endo_cluster),
            'pcos_severity': float(pcos_severity),
            'pcos_cluster': int(pcos_cluster)
        }

        return jsonify(response)

    # Add other routes similarly with stateless request handling...

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
