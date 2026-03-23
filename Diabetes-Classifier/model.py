import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.datasets import fetch_openml
import pickle
import os

FEATURE_NAMES = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

def load_data():
    """Load Pima Indians Diabetes dataset"""
    dataset = fetch_openml(name="diabetes", version=1, as_frame=True)
    X = dataset.data
    y = dataset.target

    # Print actual columns for debugging
    print(f"[DEBUG] Actual columns: {list(X.columns)}")

    # Rename columns to our expected names regardless of source format
    X.columns = FEATURE_NAMES

    # Convert target to binary 0/1
    y = (y == "tested_positive").astype(int)
    return X, y

def train_model():
    """Train Decision Tree and return model + metrics"""
    print("[INFO] Loading dataset...")
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("[INFO] Training Decision Tree...")
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
    cm = confusion_matrix(y_test, y_pred).tolist()
    report = classification_report(y_test, y_pred, output_dict=True)
    feature_importance = dict(zip(FEATURE_NAMES, [round(f, 4) for f in model.feature_importances_]))

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    print(f"[INFO] Model trained! Accuracy: {accuracy}%")

    return model, {
        "accuracy": accuracy,
        "confusion_matrix": cm,
        "classification_report": report,
        "feature_importance": feature_importance,
        "test_size": len(y_test),
        "train_size": len(y_train)
    }

def load_trained_model():
    """Load model from disk if exists, else train"""
    if os.path.exists("model.pkl"):
        print("[INFO] Loading saved model...")
        with open("model.pkl", "rb") as f:
            return pickle.load(f)
    else:
        model, _ = train_model()
        return model
