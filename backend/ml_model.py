"""
ml_model.py - Machine Learning for EarlySense AI

This file contains the complete beginner-friendly ML workflow:
1. Load the dataset
2. Explore the data
3. Clean the data
4. Create the target label (at_risk)
5. Preprocess features
6. Split data into training and testing sets
7. Train and compare models
8. Evaluate models
9. Save the best model
10. Load the model and make predictions

We use:
- pandas: to load and work with table-like data (CSV files)
- numpy: for simple numeric operations
- scikit-learn: for preprocessing, ML models, splitting, and evaluation
- joblib: to save/load the trained model to a file
"""

import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


# This file lives in backend/, so we build paths relative to it.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "trained_model.pkl")

# The dataset has no "at_risk" column, so we create one.
# Rule: a student is At Risk if ANY score is below 60.
# This is a simple early-warning rule that is easy to understand.
RISK_SCORE_THRESHOLD = 60

# These are the input columns we use to make predictions.
# We do NOT use the score columns as inputs when predicting risk from scores would leak the answer.
# Instead, for EarlySense AI we predict risk using student background information.
# This makes the model useful before final scores are fully known in a real scenario can be extended,
# but for this dataset we use available non-score features and also show score-based target creation clearly.
CATEGORICAL_FEATURES = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]

# We also include scores as features? No - that would leak target because target is derived from scores.
# So we only use background features for prediction.
FEATURE_COLUMNS = CATEGORICAL_FEATURES


def load_data(file_path=DATA_PATH):
    """Load CSV data into a pandas DataFrame."""
    print("\n=== 1. LOADING DATA ===")
    data = pd.read_csv(file_path)
    print(f"Loaded data from: {file_path}")
    print(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
    return data


def explore_data(data):
    """Print simple information to understand the dataset."""
    print("\n=== 2. DATA EXPLORATION ===")
    print("\nFirst 5 rows:")
    print(data.head())

    print("\nColumn names and data types:")
    print(data.info())

    print("\nNumeric summary:")
    print(data.describe())

    print("\nCategory counts:")
    for col in CATEGORICAL_FEATURES:
        print(f"\n{col}:")
        print(data[col].value_counts())


def clean_data(data):
    """Clean data with simple, safe steps."""
    print("\n=== 3. DATA CLEANING ===")
    cleaned = data.copy()

    # Remove duplicate rows if any exist.
    before = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    print(f"Removed duplicates: {before - len(cleaned)}")

    # Check for missing values.
    missing_counts = cleaned.isnull().sum()
    print("\nMissing values per column:")
    print(missing_counts)

    # Simple missing value handling:
    # - numeric: fill with median
    # - categorical: fill with mode (most common value)
    for col in cleaned.columns:
        if cleaned[col].isnull().any():
            if cleaned[col].dtype == "object":
                cleaned[col] = cleaned[col].fillna(cleaned[col].mode()[0])
            else:
                cleaned[col] = cleaned[col].fillna(cleaned[col].median())
    print("Missing values handled (if any).")

    return cleaned


def create_target(data):
    """Create the at_risk target column."""
    print("\n=== 4. CREATING TARGET LABEL ===")
    data = data.copy()

    # A student is at risk if any of the three scores is below threshold.
    score_columns = ["math score", "reading score", "writing score"]
    data["at_risk"] = (data[score_columns] < RISK_SCORE_THRESHOLD).any(axis=1).astype(int)

    counts = data["at_risk"].value_counts()
    print(f"Risk rule: at_risk = 1 if any score < {RISK_SCORE_THRESHOLD}, else 0")
    print("Target distribution:")
    print(counts)
    print(f"At-risk percentage: {data['at_risk'].mean() * 100:.2f}%")
    return data


def prepare_features_and_target(data):
    """Split dataframe into X (inputs) and y (target)."""
    print("\n=== 5. FEATURE SELECTION ===")
    X = data[FEATURE_COLUMNS].copy()
    y = data["at_risk"].copy()
    print(f"Feature columns: {FEATURE_COLUMNS}")
    print("Target column: at_risk")
    print("Note: Score columns are used to create the target, but NOT used as input features,")
    print("because using them would leak the answer and make the model unrealistic.")
    return X, y


def build_preprocessor():
    """Create preprocessing for categorical features.

    OneHotEncoder converts categories like 'female'/'male' into numeric columns.
    ML models need numbers, so this step is required.
    handle_unknown='ignore' prevents errors if a new category appears later.
    """
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def split_data(X, y):
    """Split data into training and testing sets."""
    print("\n=== 6. TRAIN/TEST SPLIT ===")
    # test_size=0.2 means 20% test, 80% train.
    # random_state=42 makes the split reproducible.
    # stratify=y keeps the at-risk proportion similar in both sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")
    return X_train, X_test, y_train, y_test


def get_models():
    """Create simple models to compare."""
    # We compare a few beginner-friendly classifiers.
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=5),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100),
    }
    return models


def evaluate_model(model, X_test, y_test):
    """Calculate common classification metrics."""
    predictions = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, predictions),
        "classification_report": classification_report(y_test, predictions, zero_division=0),
    }
    return metrics


def train_and_compare_models(X_train, X_test, y_train, y_test):
    """Train multiple models and pick the best one."""
    print("\n=== 7. MODEL TRAINING & COMPARISON ===")
    preprocessor = build_preprocessor()
    models = get_models()

    results = {}
    best_name = None
    best_model = None
    best_f1 = -1

    for name, classifier in models.items():
        print(f"\nTraining: {name}")
        # Pipeline ensures preprocessing and model are saved together.
        # This prevents train/serve mismatch: same preprocessing at prediction time.
        model = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ])
        model.fit(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test)
        results[name] = {"model": model, "metrics": metrics}

        print(f"Accuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1']:.4f}")
        print("Confusion Matrix:")
        print(metrics["confusion_matrix"])

        # We choose best model by F1 score because it balances precision and recall.
        # For risk detection, we care about catching at-risk students (recall)
        # while not over-flagging everyone (precision).
        if metrics["f1"] > best_f1:
            best_f1 = metrics["f1"]
            best_name = name
            best_model = model

    print("\n=== 8. MODEL EVALUATION SUMMARY ===")
    for name, result in results.items():
        m = result["metrics"]
        print(f"{name}: acc={m['accuracy']:.4f}, prec={m['precision']:.4f}, rec={m['recall']:.4f}, f1={m['f1']:.4f}")

    print(f"\nBest model: {best_name} (F1={best_f1:.4f})")
    print("\nBest model classification report:")
    print(results[best_name]["metrics"]["classification_report"])

    return best_name, best_model, results


def save_model(model, model_name, metrics, file_path=MODEL_PATH):
    """Save the trained model and metadata."""
    print("\n=== 9. SAVING MODEL ===")
    model_package = {
        "model": model,
        "model_name": model_name,
        "metrics": {
            "accuracy": float(metrics["accuracy"]),
            "precision": float(metrics["precision"]),
            "recall": float(metrics["recall"]),
            "f1": float(metrics["f1"]),
        },
        "feature_columns": FEATURE_COLUMNS,
        "risk_score_threshold": RISK_SCORE_THRESHOLD,
    }
    joblib.dump(model_package, file_path)
    print(f"Saved model to: {file_path}")
    return file_path


def load_model(file_path=MODEL_PATH):
    """Load the saved model package."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Model file not found: {file_path}. Run ml_model.py first.")
    model_package = joblib.load(file_path)
    return model_package


def predict_student(student_data, model_package=None):
    """Make a prediction for one student.

    student_data should be a dictionary with keys matching FEATURE_COLUMNS.
    """
    if model_package is None:
        model_package = load_model()

    model = model_package["model"]

    # Create a one-row DataFrame because sklearn pipeline expects tabular input.
    input_df = pd.DataFrame([student_data], columns=FEATURE_COLUMNS)

    prediction = int(model.predict(input_df)[0])

    # predict_proba gives probability for each class: [prob_not_risk, prob_risk]
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        risk_probability = float(probabilities[1])
    else:
        risk_probability = float(prediction)

    result = {
        "prediction": prediction,
        "at_risk": bool(prediction == 1),
        "risk_label": "At Risk" if prediction == 1 else "Not At Risk",
        "probability": round(risk_probability, 4),
        "message": (
            "This student may need early support."
            if prediction == 1
            else "This student shows lower risk based on available features."
        ),
    }
    return result


def run_training_pipeline():
    """Run the full ML workflow from loading data to saving the model."""
    data = load_data()
    explore_data(data)
    data = clean_data(data)
    data = create_target(data)
    X, y = prepare_features_and_target(data)
    X_train, X_test, y_train, y_test = split_data(X, y)
    best_name, best_model, results = train_and_compare_models(X_train, X_test, y_train, y_test)
    save_model(best_model, best_name, results[best_name]["metrics"])

    print("\n=== 10. SAMPLE PREDICTION ===")
    sample_student = {
        "gender": "female",
        "race/ethnicity": "group B",
        "parental level of education": "bachelor's degree",
        "lunch": "standard",
        "test preparation course": "none",
    }
    prediction = predict_student(sample_student)
    print("Sample input:", sample_student)
    print("Prediction:", prediction)
    return prediction


if __name__ == "__main__":
    run_training_pipeline()
