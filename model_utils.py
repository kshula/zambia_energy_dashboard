# model_utils.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression

def train_ensemble_model(file_path):
    # Load data
    lake = pd.read_csv(file_path)

    # Convert 'date' column to datetime format and extract features
    lake['date'] = pd.to_datetime(lake['date'])
    lake['year'] = lake['date'].dt.year
    lake['month'] = lake['date'].dt.month
    lake['day'] = lake['date'].dt.day

    # Create lag features
    lake['lag1'] = lake['Target_height_variation'].shift(1)
    lake['lag3'] = lake['Target_height_variation'].shift(3)
    lake['lag6'] = lake['Target_height_variation'].shift(6)

    # Drop rows with missing lag values
    lake.dropna(inplace=True)

    # Features and target variable
    X = lake[['year', 'month', 'day', 'lag1', 'lag3', 'lag6']]
    y = lake['Target_height_variation']

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Initialize models
    rf = RandomForestRegressor(n_estimators=200, max_depth=20, random_state=42)
    gb = GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42)
    svm = SVR(C=1.0, epsilon=0.1)

    # Train models on the entire dataset
    rf.fit(X_scaled, y)
    gb.fit(X_scaled, y)
    svm.fit(X_scaled, y)

    # Predict with each model
    rf_pred = rf.predict(X_scaled)
    gb_pred = gb.predict(X_scaled)
    svm_pred = svm.predict(X_scaled)

    # Combine predictions into a DataFrame
    predictions = pd.DataFrame({
        'rf_pred': rf_pred,
        'gb_pred': gb_pred,
        'svm_pred': svm_pred
    })

    # Train meta-model (Linear Regression) on predictions
    meta_model = LinearRegression()
    meta_model.fit(predictions, y)

    models = {'rf': rf, 'gb': gb, 'svm': svm}
    return scaler, models, meta_model,

def predict_future(data, lags, steps, scaler, models, meta_model):
    future_predictions = []
    for _ in range(steps):
        # Prepare the data for the next prediction
        data_scaled = scaler.transform(data)
        rf_pred = models['rf'].predict(data_scaled)
        gb_pred = models['gb'].predict(data_scaled)
        svm_pred = models['svm'].predict(data_scaled)
        
        # Combine predictions into a DataFrame
        future_pred = pd.DataFrame({
            'rf_pred': rf_pred,
            'gb_pred': gb_pred,
            'svm_pred': svm_pred
        })
        
        # Predict using the meta-model
        next_pred = meta_model.predict(future_pred)[-1]
        future_predictions.append(next_pred)
        
        # Update the data with the new prediction
        new_row = data.iloc[-1].copy()
        new_row['lag1'] = next_pred
        new_row['lag3'] = data['lag1'].iloc[-1]
        new_row['lag6'] = data['lag3'].iloc[-1]
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    
    return future_predictions

# Preprocess the data
def preprocess_data(file_path):
    lake = pd.read_csv(file_path)
    lake['date'] = pd.to_datetime(lake['date'])
    lake['year'] = lake['date'].dt.year
    lake['month'] = lake['date'].dt.month
    lake['day'] = lake['date'].dt.day

    # Create lag features
    lake['lag1'] = lake['Target_height_variation'].shift(1)
    lake['lag3'] = lake['Target_height_variation'].shift(3)
    lake['lag6'] = lake['Target_height_variation'].shift(6)

    # Drop rows with missing lag values
    lake.dropna(inplace=True)
    
    return lake