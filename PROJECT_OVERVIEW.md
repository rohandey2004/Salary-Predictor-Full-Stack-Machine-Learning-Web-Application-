# Salary Predictor — Project Overview

## What is this project about?

This is a **Salary Predictor** — a full-stack machine learning web application that answers one question:

> *"Given how many years of experience someone has, what salary should they expect?"*

It takes a CSV dataset of 95 real-world salary records, trains a **Linear Regression** model on it, and serves predictions through a clean web interface. A user types in their years of experience (e.g. `5.5`) and instantly gets back a predicted annual salary — along with a live chart showing where they fall on the regression line against all data points.

---

## How was it built?

The project has three layers:

| Layer | File | Tech |
|-------|------|------|
| **ML Training** | `train_model.py` | pandas, scikit-learn, joblib |
| **REST API** | `app.py` | Flask (`POST /predict`, `GET /`) |
| **Frontend UI** | `templates/index.html` | HTML/CSS, Chart.js, fetch API |

1. **`train_model.py`** loads the CSV, splits it 80/20, fits a `LinearRegression`, prints evaluation metrics, and saves the model to `model.pkl`
2. **`app.py`** loads `model.pkl` once at startup, validates incoming requests, runs predictions, and also serves the HTML page — single server, no CORS needed
3. **`templates/index.html`** renders a styled card with a number input + button, calls the Flask API via `fetch`, shows the formatted salary result, and plots all 95 data points as a scatter chart with the regression line and a red highlight for the user's prediction

---

## Why was it built this way?

| Decision | Reason |
|----------|--------|
| **Linear Regression** | The relationship between experience and salary in the dataset is strongly linear — R² of **0.9736** confirms it fits extremely well |
| **Flask as single server** | Keeps the setup simple — one `python app.py` command, no separate frontend server, no CORS configuration |
| **Chart.js for the chart** | Lightweight CDN library, no build step needed, renders scatter + line datasets natively |
| **joblib for model persistence** | Standard scikit-learn recommended serialization — fast, reliable, one line to save and load |
| **80/20 train/test split** | Industry-standard split to evaluate generalization without overfitting to the full dataset |

---

## Model Performance

| Metric | Value |
|--------|-------|
| Algorithm | Linear Regression |
| R² Score (test set) | 0.9736 |
| Mean Absolute Error | $3,764 |
| Slope | $11,745 / yr |
| Intercept | $16,686 |
| Training samples | 76 / 95 |
| Test samples | 19 / 95 |

The model achieves a **Mean Absolute Error of $3,764** — meaning on average, predictions are within ~$3.7k of the actual salary, which is strong for a single-feature linear model.
