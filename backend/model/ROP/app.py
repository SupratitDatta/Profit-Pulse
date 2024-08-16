from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app)

# Load and prepare the dataset and model
df = pd.read_csv("project.csv", encoding="latin1")
np.random.seed(42)
df['quantity'] = np.random.randint(250, 400, size=len(df))
df['TOTAL_DAYS'] = np.random.randint(20, 45, size=len(df))
df['Demand_rate'] = (df['quantity'] / df["TOTAL_DAYS"]).round()
df['SERVICE_LEVEL'] = np.random.randint(85, 95, size=len(df))
mean_service_level = df['SERVICE_LEVEL'].mean()
std_dev_service_level = df['SERVICE_LEVEL'].std()
df['Service_level_Z_score'] = ((df['SERVICE_LEVEL'] - mean_service_level) / std_dev_service_level)
df['DAYS_REQ_TO_RECIVE_ORDER'] = np.random.randint(15, 25, size=len(df))
std_dev_demand_rate = df['Demand_rate'].std()
df['Safety_stock'] = np.abs(std_dev_demand_rate * df['Service_level_Z_score'] * np.sqrt(df['DAYS_REQ_TO_RECIVE_ORDER']))
df['ROP'] = (df['Demand_rate'] * df['DAYS_REQ_TO_RECIVE_ORDER']) + df['Safety_stock']
df = df.drop(columns=['SERVICE_LEVEL', 'Service_level_Z_score', 'TOTAL_DAYS'])
X = df[['quantity', 'Demand_rate', 'DAYS_REQ_TO_RECIVE_ORDER', 'Safety_stock']]
y = df['ROP']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

@app.route('/api/rop/predict', methods=['POST'])
def predict():
    # Extract JSON data from the request
    data = request.json
    quantity = float(data['quantity'])
    demand_rate = float(data['demand_rate'])
    days_req_to_receive_order = float(data['days_req_to_receive_order'])
    safety_stock = float(data['safety_stock'])

    # Prepare input data for the model
    input_data = np.array([[quantity, demand_rate, days_req_to_receive_order, safety_stock]])
    prediction = model.predict(input_data)[0]

    # Return the prediction as JSON
    return jsonify({'rop': prediction})

if __name__ == '__main__':
    app.run(debug=True, port=5000)