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
    with open("./models/GradientBoosting_model.pkl", "rb") as file:
        clf = pickle.load(file)

    with open("./models/AdaBoost_model.pkl", "rb") as file:
        abc = pickle.load(file)

    with open("./models/logistic_regression_model.pkl", "rb") as file:
        logistic_regression = pickle.load(file)

    with open("./models/KMeans_model.pkl", "rb") as file:
        kmeans = pickle.load(file)

    with open("./models/scaler.pkl", "rb") as file:
        scaler = pickle.load(file)

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    severity_model = pickle.load(
        open(os.path.join(APP_ROOT, "./models/endo_LR.pkl"), "rb")
    )
    cluster_model = pickle.load(
        open(os.path.join(APP_ROOT, "./models/endo_LR_cluster.pkl"), "rb")
    )

    # === Template JSON Data ===
    ENDO_CLUSTER_JSON = {...}  # your original dict here
    ENDO_PREDICT_JSON = {...}
    PCOS_PREDICT_JSON = {...}

    # Store copies to reset later
    ENDO_CLUSTER_JSON_NULL = ENDO_CLUSTER_JSON.copy()
    ENDO_PREDICT_JSON_NULL = ENDO_PREDICT_JSON.copy()
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

    @app.route("/update", methods=["POST"])
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
        return jsonify(
            {
                "Updated cluster json": make_json_safe(ENDO_CLUSTER_JSON),
                "Updated predict json": make_json_safe(ENDO_PREDICT_JSON),
                "Updated pcos json": make_json_safe(PCOS_PREDICT_JSON),
            }
        )

    @app.route("/submit", methods=["POST"])
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
            "endo_severity": endo_severity,
            "endo_cluster": endo_cluster,
            "pcos_severity": pcos_severity,
            "pcos_cluster": pcos_cluster,
        }

        return jsonify(
            {
                k: (v.tolist() if isinstance(v, np.ndarray) else v)
                for k, v in response.items()
            }
        )

    @app.route("/endoseverity", methods=["POST"])
    def endo_predict():
        data = request.get_json()
        features = [int(x or 0) for x in data.values()]
        df = pd.DataFrame([features], columns=data.keys())
        severity = severity_model.predict_proba(df)[0][1]
        return jsonify({"severity": severity})

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # Use PORT from env or default 5000
    app.run(host="0.0.0.0", port=port, debug=False)
