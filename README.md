# EarlySense AI

EarlySense AI is a beginner-friendly machine learning web application that predicts whether a student may be **At Risk** based on background and test preparation information. The project combines a React frontend, a FastAPI backend, and a Scikit-learn training pipeline in one simple, integrated codebase.

## Project Overview

The application uses the Students Performance dataset stored in `backend/data.csv`. The original dataset does not include an at-risk label, so the project creates one during training using a clear rule: a student is marked **At Risk** if any of the three scores (`math score`, `reading score`, or `writing score`) is below 60.

To avoid data leakage, the score columns are used only to create the target label. They are **not** used as input features for prediction. The model predicts risk from background and preparation features that are available in the form.

## Features

- **End-to-end ML workflow**: Load, explore, clean, preprocess, split, train, compare, evaluate, save, load, and predict in `backend/ml_model.py`.
- **Simple FastAPI backend**: Health, model info, and prediction endpoints in `backend/main.py`.
- **React frontend**: Form-based interface for entering student details and viewing prediction results.
- **Saved model artifact**: The best trained model is saved as `backend/trained_model.pkl`.
- **Beginner-friendly structure**: Small project layout with clear file responsibilities.

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Pydantic

### Frontend

- React
- Vite
- JavaScript
- CSS

## Project Structure

```text
EarlySense-AI/
├── .gitignore
├── README.md
├── backend/
│   ├── data.csv
│   ├── main.py
│   ├── ml_model.py
│   ├── requirements.txt
│   └── trained_model.pkl                # Generated after training
└── frontend/
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    └── src/
        ├── App.css
        ├── App.jsx
        ├── main.jsx
        ├── components/
        │   ├── ErrorBoundary.jsx
        │   ├── PredictionResult.jsx
        │   └── StudentForm.jsx
        └── services/
            └── api.js
```

## Machine Learning Workflow

The ML workflow is implemented in `backend/ml_model.py`:

1. **Load data**: Reads the dataset from `backend/data.csv`.
2. **Explore data**: Prints shape, sample rows, column info, summary statistics, and category counts.
3. **Clean data**: Removes duplicates and handles missing values with simple rules.
4. **Create target label**: Adds `at_risk = 1` when any score is below 60; otherwise `at_risk = 0`.
5. **Select features**: Uses only background/preparation features as inputs.
6. **Preprocess features**: Uses a Scikit-learn `ColumnTransformer` with `OneHotEncoder(handle_unknown="ignore")` for categorical features.
7. **Split data**: Uses `train_test_split` with a fixed random state and stratification.
8. **Train and compare models**: Trains Logistic Regression, Decision Tree, and Random Forest using the same pipeline structure.
9. **Evaluate models**: Calculates accuracy, precision, recall, F1 score, confusion matrix, and classification report.
10. **Save best model**: Selects the best model by F1 score and saves it with metadata using Joblib.
11. **Predict**: Loads the saved model and returns prediction, risk label, probability, and message.

## Input Features

The prediction form sends these fields to the backend:

- `gender`
- `race/ethnicity`
- `parental level of education`
- `lunch`
- `test preparation course`

## Prerequisites

- Python 3.10 or later
- Node.js 18 or later
- npm
- Windows PowerShell

## Setup and Run

### 1. Backend Setup and Model Training

Open PowerShell and run:

```powershell
cd C:\Users\shrey\Desktop\student_eval\EarlySense-AI\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ml_model.py
```

This creates the virtual environment, installs dependencies, trains the models, prints evaluation results, and saves `backend/trained_model.pkl`.

### 2. Run the FastAPI Backend

In the same backend terminal (with the virtual environment activated), run:

```powershell
cd C:\Users\shrey\Desktop\student_eval\EarlySense-AI\backend
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8001
```

The backend will be available at:

- API base URL: `http://127.0.0.1:8001`
- Swagger docs: `http://127.0.0.1:8001/docs`

### 3. Run the React Frontend

Open a new PowerShell window and run:

```powershell
cd C:\Users\shrey\Desktop\student_eval\EarlySense-AI\frontend
npm install
npm run dev -- --port 5174 --host 127.0.0.1
```

The frontend will be available at:

- Frontend URL: `http://127.0.0.1:5174`

## API Documentation

### Available Endpoints

- `GET /health` - Returns API status and whether the model is loaded.
- `GET /model-info` - Returns model name, saved metrics, feature columns, and risk threshold.
- `POST /predict` - Accepts student input and returns a risk prediction.

### Example Prediction Request

```json
{
  "gender": "female",
  "race/ethnicity": "group B",
  "parental level of education": "bachelor's degree",
  "lunch": "standard",
  "test preparation course": "none"
}
```

### Example Prediction Response

```json
{
  "prediction": 0,
  "at_risk": false,
  "risk_label": "Not At Risk",
  "probability": 0.2696,
  "message": "This student shows lower risk based on available features."
}
```

## Troubleshooting

- **`ModuleNotFoundError`**: Make sure the virtual environment is activated and run `pip install -r requirements.txt`.
- **Model file not found**: Run `python ml_model.py` from the `backend` folder to generate `trained_model.pkl`.
- **Frontend cannot reach backend**: Confirm the backend is running on `127.0.0.1:8001` and check `frontend/src/services/api.js`.
- **Port already in use**: Start the backend or frontend on a different port, then update `frontend/src/services/api.js` and CORS origins in `backend/main.py` if needed.
- **PowerShell script activation blocked**: Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate the virtual environment again.
- **Blank page or stale UI**: Hard refresh the browser with `Ctrl+F5` and check the browser console for errors.

## Limitations

- This is an educational/demo project, not a production student intervention system.
- The `at_risk` label is derived from a simple score threshold (`any score < 60`), not from real intervention outcomes.
- Predictions are based only on background and preparation features available in the dataset, so predictive power is limited.
- The result should be treated as an early-warning signal, not a final judgment about a student.
