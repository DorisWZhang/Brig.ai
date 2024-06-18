from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load pre-trained models and scaler
with open('GradientBoosting_model.pkl', 'rb') as file:
    clf = pickle.load(file)

with open('KMeans_model.pkl', 'rb') as file:
    kmeans = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

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
            print("Prediction probabilities:", prediction_probabilities)  # Debug print

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

            # Predict cluster using the kmeans model
            cluster_predictions = kmeans.predict(df_scaled)
            print("Cluster predictions:", cluster_predictions)  # Debug print

            # Convert predictions to a list
            cluster_predictions_list = cluster_predictions.tolist()
            return jsonify({'cluster_predictions': cluster_predictions_list})
        else:
            return jsonify({'error': 'Input data should be a list of dictionaries'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
