import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load the CSV
df = pd.read_csv("/home/scholar/Documents/DOCS/Projects101/Projects/Disease-Prediction-AI/backend/health_data.csv")

# Check for nulls
if df.isnull().sum().sum() > 0:
    df = df.dropna()

# Features and target
X = df[["Gender", "Age", "BMI", "Glucose", "BloodPressure", "FamilyHistory"]]
y = df["Diabetes"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
model_path = os.path.join(os.getcwd(), "diabetes_model.pkl")
joblib.dump(model, model_path)

print(f"✅ Model trained and saved to: {model_path}")
