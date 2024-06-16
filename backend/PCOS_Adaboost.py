import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import metrics
import pickle

# Load the CSV file into a DataFrame
file_path = '/home/laurenyip/AI4GOODLAB/AI4GOOD_projects/Project/ai4good/backend/PCOS_data.csv'
df = pd.read_csv(file_path)
print("DataFrame loaded successfully.")

# Extract the label
label_pcos = df["PCOS (Y/N)"]

# Drop unnecessary columns
columns_to_drop = [
    "Sl. No", "Patient File No.", "PCOS (Y/N)", "Unnamed: 44", "II    beta-HCG(mIU/mL)", 
    "AMH(ng/mL)", "Endometrium (mm)", "Avg. F size (R) (mm)", "Avg. F size (L) (mm)", 
    "Follicle No. (R)", "Follicle No. (L)", "RBS(mg/dl)", "PRG(ng/mL)", "Vit D3 (ng/mL)", 
    "PRL(ng/mL)", "AMH(ng/mL)", "TSH (mIU/L)", "FSH/LH", "LH(mIU/mL)", "FSH(mIU/mL)", 
    "II    beta-HCG(mIU/mL)", "  I   beta-HCG(mIU/mL)", "Hb(g/dl)"
]
df.drop(columns=columns_to_drop, axis=1, inplace=True)

# Fill missing values
df['Marraige Status (Yrs)'] = df['Marraige Status (Yrs)'].fillna(df['Marraige Status (Yrs)'].median())
df['Fast food (Y/N)'] = df['Fast food (Y/N)'].fillna(1)

# Print the first 5 rows of the DataFrame
print(df.head(5))

# Split the dataset into features and target
X = df.values  # Features (all columns except the last)
y = label_pcos.values  # Target

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42) # 70% training and 30% test

# Initialize the AdaBoost Classifier with DecisionTreeClassifier
abc = AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1), n_estimators=50, learning_rate=1, algorithm='SAMME')

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 150],
    'learning_rate': [0.01, 0.1, 1, 10],
    'estimator__max_depth': [1, 2, 3]
}
grid_search = GridSearchCV(estimator=abc, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# Train the best AdaBoost Classifier
best_model.fit(X_train, y_train)

# Save the trained AdaBoost model
with open('AdaBoost_model.pkl', 'wb') as file:
    pickle.dump(best_model, file)

# Predict the response for the test dataset
y_pred = best_model.predict(X_test)

# Calculate train and test accuracy
train_accuracy = best_model.score(X_train, y_train)
test_accuracy = best_model.score(X_test, y_test)

# Model Accuracy
print(f"Train accuracy: {train_accuracy:.2%}, Test accuracy: {test_accuracy:.2%}")
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
