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
            prediction = clf.predict(df)
            print("Predictions:", prediction)  # Debug print
            return jsonify({'prediction': prediction.tolist()})
        else:
            return jsonify({'error': 'Input data should be a list of dictionaries'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
