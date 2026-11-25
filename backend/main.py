"""
main.py - FastAPI backend for EarlySense AI

This file creates a simple web API so the React frontend can send student data
and receive a risk prediction from our trained machine learning model.

We use:
- FastAPI: to create API endpoints easily
- Pydantic: to validate incoming request data
- CORS middleware: to allow the React frontend (different port) to call this API
- ml_model.py: where we load the model and make predictions
"""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ml_model import FEATURE_COLUMNS, MODEL_PATH, load_model, predict_student, run_training_pipeline


# Create the FastAPI application.
app = FastAPI(title="EarlySense AI API", version="1.0.0")

# CORS allows the frontend (running on Vite's default port) to communicate with backend.
# Without this, browser blocks requests between different ports.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model validates input data types and allowed values.
class StudentInput(BaseModel):
    gender: str = Field(..., description="Student gender")
    race_ethnicity: str = Field(..., alias="race/ethnicity", description="Race/ethnicity group")
    parental_level_of_education: str = Field(..., alias="parental level of education")
    lunch: str = Field(..., description="Lunch type")
    test_preparation_course: str = Field(..., alias="test preparation course")

    class Config:
        populate_by_name = True


# We store the loaded model in a simple variable.
model_package = None


@app.on_event("startup")
def startup_event():
    """Load the ML model when the API starts."""
    global model_package
    try:
        if not os.path.exists(MODEL_PATH):
            # If model is missing, train it automatically for convenience.
            print("Model not found. Training model...")
            run_training_pipeline()
        model_package = load_model(MODEL_PATH)
        print(f"Model loaded: {model_package.get('model_name')}")
    except Exception as e:
        print(f"Error loading model: {e}")
        model_package = None


@app.get("/health")
def health_check():
    """Simple endpoint to confirm API is running."""
    return {
        "status": "ok",
        "model_loaded": model_package is not None,
        "model_name": model_package.get("model_name") if model_package else None,
    }


@app.get("/model-info")
def model_info():
    """Return basic information about the trained model."""
    if model_package is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    return {
        "model_name": model_package.get("model_name"),
        "metrics": model_package.get("metrics"),
        "feature_columns": model_package.get("feature_columns"),
        "risk_score_threshold": model_package.get("risk_score_threshold"),
    }


@app.post("/predict")
def predict(student: StudentInput):
    """Predict whether a student is at risk."""
    if model_package is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")

    try:
        # Convert validated Pydantic object to a plain dictionary.
        student_data = student.model_dump(by_alias=True)

        # Keep only the features the model expects.
        model_input = {col: student_data[col] for col in FEATURE_COLUMNS}

        result = predict_student(model_input, model_package=model_package)
        return result
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
