from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import pandas as pd
import numpy as np

def create_app():
    app = Flask(__name__)
    CORS(app)

    # === Load Models & Scalers ===
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
    severity_model = pickle.load(open(os.path.join(APP_ROOT, "./models/endo_LR.pkl"), 'rb'))
    cluster_model = pickle.load(open(os.path.join(APP_ROOT, "./models/endo_LR_cluster.pkl"), 'rb'))

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

    def make_json_safe(obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: make_json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_json_safe(i) for i in obj]
        else:
            return obj

    @app.route('/update', methods=['POST'])
    def update():
        input_data = request.get_json()

        for key in input_data:
            if key in ENDO_CLUSTER_JSON:
                ENDO_CLUSTER_JSON[key] = input_data[key]
            if key in ENDO_PREDICT_JSON:
                ENDO_PREDICT_JSON[key] = input_data[key]
            if key in PCOS_PREDICT_JSON:
                PCOS_PREDICT_JSON[key] = input_data[key]

        # Return updated JSONs with sets converted to lists if any
        return jsonify({
            'Updated cluster json': make_json_safe(ENDO_CLUSTER_JSON),
            'Updated predict json': make_json_safe(ENDO_PREDICT_JSON),
            'Updated pcos json': make_json_safe(PCOS_PREDICT_JSON)
        })

    @app.route('/submit', methods=['POST'])
    def submit_final():
        input_data = request.get_json()

        for key in input_data:
            if key in ENDO_CLUSTER_JSON:
                ENDO_CLUSTER_JSON[key] = input_data[key]
            if key in ENDO_PREDICT_JSON:
                ENDO_PREDICT_JSON[key] = input_data[key]
            if key in PCOS_PREDICT_JSON:
                PCOS_PREDICT_JSON[key] = input_data[key]

        # === Endometriosis Prediction ===
        endo_features = [int(x or 0) for x in ENDO_PREDICT_JSON.values()]
        endo_df = pd.DataFrame([endo_features], columns=ENDO_PREDICT_JSON.keys())
        endo_severity = severity_model.predict_proba(endo_df)[0][1]
        # Reset after use
        for k in ENDO_PREDICT_JSON:
            ENDO_PREDICT_JSON[k] = ENDO_PREDICT_JSON_NULL[k]

        # === Endo Clustering ===
        cluster_features = [[int(x or 0) for x in ENDO_CLUSTER_JSON.values()]]
        endo_cluster = int(np.argmax(cluster_model.predict_proba(cluster_features)[0]))
        for k in ENDO_CLUSTER_JSON:
            ENDO_CLUSTER_JSON[k] = ENDO_CLUSTER_JSON_NULL[k]

        # === PCOS Prediction ===
        pcos_features = [int(x or 0) for x in PCOS_PREDICT_JSON.values()]
        pcos_df = pd.DataFrame([pcos_features], columns=PCOS_PREDICT_JSON.keys())
        pcos_df.columns = pcos_df.columns.str.strip()
        pcos_scaled = scaler.transform(pcos_df)
        pcos_severity = abc.predict_proba(pcos_scaled)[0][1]

        # === PCOS Cluster ===
        logistic_preds = logistic_regression.predict(pcos_scaled).reshape(1, -1)
        pcos_cluster = kmeans.predict(logistic_preds).tolist()[0]
        for k in PCOS_PREDICT_JSON:
            PCOS_PREDICT_JSON[k] = PCOS_PREDICT_JSON_NULL[k]

        response = {
            'endo_severity': endo_severity,
            'endo_cluster': endo_cluster,
            'pcos_severity': pcos_severity,
            'pcos_cluster': pcos_cluster
        }

        return jsonify({k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in response.items()})

    @app.route('/endoseverity', methods=['POST'])
    def endo_predict():
        data = request.get_json()
        features = [int(x or 0) for x in data.values()]
        df = pd.DataFrame([features], columns=data.keys())
        severity = severity_model.predict_proba(df)[0][1]
        return jsonify({'severity': severity})

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # Use PORT from env or default 5000
    app.run(host='0.0.0.0', port=port, debug=False)
