import joblib
from flask import Flask, request, jsonify, render_template, abort
import numpy as np
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

model = joblib.load('random_forest_model.joblib')

def postprocess(predictions):
    if(predictions == 1):
        return "Loan Denied"
    else:
        return "Loan Approve"

def predict(model, input_data):
    predictions = model.predict(input_data)
    final_output = postprocess(predictions)
    return final_output

def create_gemini_prompt(data, prediction):
    DataDescription = "credit_grade: 4 is the best and 0 being the worst, employment: 0 is unemployed 1 is Self-employed 2 is Salaried"
    prompt = f"DataDescription:{DataDescription}\nData: {data}\nPrediction: {prediction}\nProvide a 2-3 line analysis of the data and justify the corresponding prediction."
    return prompt

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
llm_model = genai.GenerativeModel('gemini-1.5-flash')

@app.before_request
def check_forwarded_headers():
    if not request.headers.get('X-Forwarded-For'):
        abort(403)  # Forbidden

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/predict', methods=['POST'])
def predict_api():
    try:
        # Get JSON input
        input_json = request.json
        input_data = np.array([int(value) for value in input_json.values()])
        n = input_data.shape[0]
        input_data = input_data.reshape(1, n)
        result = predict(model, input_data)
        prompt = create_gemini_prompt(input_json,result)
        response = llm_model.generate_content(prompt)
        return jsonify({'prediction': result, 'description': response.text})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)