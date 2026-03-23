from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Optional
import numpy as np
from model import train_model, FEATURE_NAMES
import pickle
import os

app = FastAPI(
    title="Diabetes Prediction API",
    description="Decision Tree Classifier for Diabetes Prediction",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Train model and store metrics on startup
print("[STARTUP] Training model...")
model, metrics = train_model()
print("[STARTUP] Model ready!")


# ── Pydantic Model ───────────────────────────────────────────────

class PatientData(BaseModel):
    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: float

    @validator("glucose")
    def glucose_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Glucose must be greater than 0")
        return v

    @validator("bmi")
    def bmi_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("BMI must be greater than 0")
        return v

    @validator("age")
    def age_must_be_valid(cls, v):
        if v < 1 or v > 120:
            raise ValueError("Age must be between 1 and 120")
        return v


# ── Routes ───────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Diabetes Prediction API is running 🩺"}


@app.post("/predict")
def predict(patient: PatientData):
    """Predict diabetes risk for a patient"""
    features = np.array([[
        patient.pregnancies,
        patient.glucose,
        patient.blood_pressure,
        patient.skin_thickness,
        patient.insulin,
        patient.bmi,
        patient.diabetes_pedigree,
        patient.age
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    return {
        "prediction": int(prediction),
        "result": "Diabetic" if prediction == 1 else "Not Diabetic",
        "confidence": {
            "not_diabetic": round(float(probability[0]) * 100, 2),
            "diabetic": round(float(probability[1]) * 100, 2)
        },
        "risk_level": (
            "High" if probability[1] > 0.7 else
            "Medium" if probability[1] > 0.4 else
            "Low"
        )
    }


@app.get("/metrics")
def get_metrics():
    """Get model performance metrics"""
    return metrics


@app.get("/features")
def get_features():
    """Get feature importance from the model"""
    return {
        "features": FEATURE_NAMES,
        "importance": metrics["feature_importance"]
    }
