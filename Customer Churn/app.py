from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('Customer_Churn_Prediction.pkl', 'rb'))

# Predefined mapping for Geography, HasCrCard, and IsActiveMember
geography_mapping = {
    'France': 0,
    'Germany': 1,
    'Spain': 2
}

hasCreditCard_mapping = {
    'Yes': 1,
    'No': 0
}

isActiveMember_mapping = {
    'Yes': 1,
    'No': 0
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Retrieve form data
        form_data = {
            'CreditScore': request.form.get('CreditScore', ''),
            'Age': request.form.get('Age', ''),
            'Tenure': request.form.get('Tenure', ''),
            'Balance': request.form.get('Balance', ''),
            'NumOfProducts': request.form.get('NumOfProducts', ''),
            'HasCrCard': request.form.get('HasCrCard', ''),
            'IsActiveMember': request.form.get('IsActiveMember', ''),
            'EstimatedSalary': request.form.get('EstimatedSalary', ''),
            'Geography': request.form.get('Geography', '')
        }

        # Map 'Geography', 'HasCrCard', and 'IsActiveMember' to predefined numeric values
        geo_value = geography_mapping.get(form_data['Geography'], -1)
        hasCreditCard_value = hasCreditCard_mapping.get(form_data['HasCrCard'], -1)
        isActiveMember_value = isActiveMember_mapping.get(form_data['IsActiveMember'], -1)

        # Check for invalid values
        if geo_value == -1 or hasCreditCard_value == -1 or isActiveMember_value == -1:
            return render_template('index.html', prediction_message='Invalid input values', form_data=form_data)

        # Prepare the input data
        data = np.array([[int(form_data['CreditScore']),
                          int(form_data['Age']),
                          int(form_data['Tenure']),
                          float(form_data['Balance']),
                          int(form_data['NumOfProducts']),
                          hasCreditCard_value,
                          isActiveMember_value,
                          float(form_data['EstimatedSalary']),
                          geo_value]])

        # Make prediction and get probability
        prediction_proba = model.predict_proba(data)[0]
        prediction = model.predict(data)[0]

        # Create a message based on the prediction
        if prediction == 1:
            prediction_message = f'Probability of Customer leaving is {prediction_proba[1] * 100:.2f}%.'
        else:
            prediction_message = f'Probability of Customer leaving is {prediction_proba[0] * 100:.2f}%.'

        # Return the result with form data
        return render_template('index.html', prediction_message=prediction_message, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
