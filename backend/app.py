from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the logistic regression model from the pickle file
with open('Pcos_LR.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return "<h1>hello</h1>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.json
        # Extract features from the JSON data and convert to numpy array
        input_features = np.array(data['features']).reshape(1, -1)
        # Use the model to predict the class
        prediction = model.predict(input_features)
        # Return the prediction result as JSON
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        # If there's an error, return an error message
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
