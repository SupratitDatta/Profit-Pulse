from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

# Load and preprocess data
df = pd.read_csv("project.csv", encoding="latin1")
df['actual_price'] = pd.to_numeric(df['actual_price'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)
df['selling_price'] = pd.to_numeric(df['selling_price'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)
df['selling_price'] *= 6
df['description'] = df['description'].str.replace('% off', '')
df['description'] = df['description'].fillna('0').astype(int)
df['quantity'] = np.random.randint(10, 20, size=len(df))
df['marketing_price'] = np.random.randint(500, 700, size=len(df))
df['initial_price'] = df['actual_price'] * df['quantity']
df['raw_sell_price'] = np.random.randint(30000, 70000, size=len(df))
df['discounted_price'] = df['selling_price'] * (1 - df['description'] / 100)
df['final_selling_price'] = df['raw_sell_price'] - df['discounted_price']
df['profit'] = df['final_selling_price'] - (df['initial_price'] + df['marketing_price'])
df['investment'] = df['initial_price'] + df['marketing_price']
df['ROI'] = (df['profit'] / df['investment']) * 100

# Prepare data for the model
columns = ['initial_price', 'raw_sell_price', 'discounted_price', 'profit', 'investment']
df_new = df[columns + ['ROI']]
X = df_new.drop('ROI', axis=1)
y = df_new['ROI']

# Train the model
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = LinearRegression()
model.fit(X_scaled, y)

@app.route('/api/roi/predict', methods=['POST'])
def predict():
    data = request.json
    initial_price = float(data['initialPrice'])
    raw_sell_price = float(data['rawSellPrice'])
    discounted_price = float(data['discountedPrice'])
    profit = float(data['profit'])
    investment = float(data['investment'])
    
    # Prepare input for the model
    input_data = np.array([[initial_price, raw_sell_price, discounted_price, profit, investment]])
    input_scaled = scaler.transform(input_data)
    
    # Predict ROI
    prediction = model.predict(input_scaled)[0]
    
    return jsonify({'roi': prediction})

if __name__ == '__main__':
    app.run(debug=True, port=5005)