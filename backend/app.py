from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load pre-trained model
with open('AdaBoost_model.pkl', 'rb') as file:
    clf = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if isinstance(data, list):  # Ensure that the input is a list
            df = pd.DataFrame(data)
            print("Received data:", df)  # Debug print

            # Ensure that column names are stripped of leading/trailing whitespace
            df.columns = df.columns.str.strip()

            # Predict probabilities using the classifier
            prediction_probabilities = clf.predict_proba(df)
            print("Prediction probabilities:", prediction_probabilities)  # Debug print

            # Convert probabilities to a list of lists, negative, positive
            prediction_probabilities_list = prediction_probabilities.tolist()
            return jsonify({'prediction_probabilities': prediction_probabilities_list})
        else:
            return jsonify({'error': 'Input data should be a list of dictionaries'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
