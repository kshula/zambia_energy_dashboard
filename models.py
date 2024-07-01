import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load data
file_path = 'data\lake.csv'
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

# Split data into training and testing sets (80:20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize models
rf = RandomForestRegressor(n_estimators=200, max_depth=20, random_state=42)
gb = GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42)
svm = SVR(C=1.0, epsilon=0.1)

# Train models
rf.fit(X_train_scaled, y_train)
gb.fit(X_train_scaled, y_train)
svm.fit(X_train_scaled, y_train)

# Predict with each model
rf_pred = rf.predict(X_test_scaled)
gb_pred = gb.predict(X_test_scaled)
svm_pred = svm.predict(X_test_scaled)

# Combine predictions into a DataFrame
predictions = pd.DataFrame({
    'rf_pred': rf_pred,
    'gb_pred': gb_pred,
    'svm_pred': svm_pred
})

# Train meta-model (Linear Regression) on predictions
meta_model = LinearRegression()
meta_model.fit(predictions, y_test)

# Final ensemble prediction
ensemble_pred = meta_model.predict(predictions)

# Evaluate the ensemble model
mse_ensemble = mean_squared_error(y_test, ensemble_pred)
print(f'Ensemble Model: MSE = {mse_ensemble}')

# Display individual model MSEs for comparison
results = {
    'Random Forest': mean_squared_error(y_test, rf_pred),
    'Gradient Boosting': mean_squared_error(y_test, gb_pred),
    'Support Vector Machine': mean_squared_error(y_test, svm_pred),
    'Ensemble': mse_ensemble
}

results_df = pd.DataFrame(list(results.items()), columns=['Model', 'MSE'])
print(results_df)

# Optional: Save results to CSV
results_df.to_csv('model_evaluation_results.csv', index=False)
