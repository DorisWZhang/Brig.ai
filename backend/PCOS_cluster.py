import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
import seaborn as sns
import pickle

# Load the CSV file into a DataFrame
file_path = '/home/laurenyip/AI4GOODLAB/AI4GOOD_projects/Project/ai4good/backend/PCOS_data.csv'
df = pd.read_csv(file_path)
print("DataFrame loaded successfully.")

# Clean column names
df.columns = df.columns.str.strip()

# Extract the label
label_pcos = df["PCOS (Y/N)"]

# Drop unnecessary columns if they exist
columns_to_drop = [
    "Sl. No", "Patient File No.", "PCOS (Y/N)", "Unnamed: 44", "II    beta-HCG(mIU/mL)", 
    "AMH(ng/mL)", "Endometrium (mm)", "Avg. F size (R) (mm)", "Avg. F size (L) (mm)", 
    "Follicle No. (R)", "Follicle No. (L)", "RBS(mg/dl)", "PRG(ng/mL)", "Vit D3 (ng/mL)", 
    "PRL(ng/mL)", "AMH(ng/mL)", "TSH (mIU/L)", "FSH/LH", "LH(mIU/mL)", "FSH(mIU/mL)", 
    "II    beta-HCG(mIU/mL)", "I   beta-HCG(mIU/mL)", "Hb(g/dl)"
]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], axis=1)

# Fill missing values
df['Marraige Status (Yrs)'] = df['Marraige Status (Yrs)'].fillna(df['Marraige Status (Yrs)'].median())
df['Fast food (Y/N)'] = df['Fast food (Y/N)'].fillna(1)

# Print dataset shape
print("PCOS dataset:\n", df.shape[0], "Records\n", df.shape[1], "Features")

# Handle missing values if any
numerical_columns = df.select_dtypes(include=['number']).columns
if len(numerical_columns) > 0:
    imputer = SimpleImputer(strategy='median')
    df[numerical_columns] = imputer.fit_transform(df[numerical_columns])

categorical_columns = df.select_dtypes(include=['object']).columns
if len(categorical_columns) > 0:
    imputer = SimpleImputer(strategy='most_frequent')
    df[categorical_columns] = imputer.fit_transform(df[categorical_columns])

# Encode non-numeric columns using one-hot encoding
df_encoded = pd.get_dummies(df)

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_encoded)

# Save the scaler to a file
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

# Assuming the last column is the target variable and the rest are features
X = df_scaled
y = label_pcos.values  # Target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Define the parameter grid for GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.001, 0.01, 0.1, 0.2],
    'max_depth': [3, 4, 5]
}

# Initialize the Gradient Boosting Classifier
gbc = GradientBoostingClassifier(random_state=0)

# Initialize GridSearchCV
grid_search = GridSearchCV(estimator=gbc, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)

# Train the model using GridSearchCV
grid_search.fit(X_train, y_train)

# Get the best model from GridSearchCV
best_gbc = grid_search.best_estimator_

# Make predictions with the best model
y_pred = best_gbc.predict(X_test)

# Evaluate the best model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Print the results
print(f"Best Parameters: {grid_search.best_params_}")
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

# Save the trained model
with open('GradientBoosting_model.pkl', 'wb') as file:
    pickle.dump(best_gbc, file)

# Train KMeans model
optimal_clusters = 2
kmeans = KMeans(n_clusters=optimal_clusters, random_state=0)
kmeans.fit(X)

# Save the KMeans model
with open('KMeans_model.pkl', 'wb') as file:
    pickle.dump(kmeans, file)

# Make a single prediction (example)
row_index = 0
row = X_test[row_index].reshape(1, -1)
prediction_prob = best_gbc.predict_proba(row)
print(f"Prediction probabilities for row {row_index}: {prediction_prob}")
