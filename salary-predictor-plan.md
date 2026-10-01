# Salary Predictor — ML Project Plan

## Overview

Build a complete, self-contained machine learning project that:
1. Trains a **Linear Regression** model on `salary_data.csv` (YearsExperience → Salary).
2. Persists the trained model as `model.pkl`.
3. Exposes a **Flask REST API** (`POST /predict`) and serves the frontend from the same server.
4. Provides an **interactive HTML/CSS/JS frontend** with a year-of-experience input, a predicted salary output, and a **Chart.js** scatter plot overlaid with the regression line.

**Dataset:** `salary_data.csv` — 95 rows, columns `YearsExperience` (float 1.1–10.5) and `Salary` (int).  
**Stack:** Python 3, scikit-learn, pandas, joblib, Flask, Chart.js (CDN).

---

## Sub-Task 1 — Model Training Script

**Status:** [x] done

### Intent
Create `train_model.py` that loads the CSV, trains a `LinearRegression` model, evaluates it, and saves the artifact so the Flask server can load it at runtime.

### Expected Outcomes
- `train_model.py` exists and runs without errors with `python train_model.py`.
- `model.pkl` is created in the project root.
- Console prints R² score and Mean Absolute Error.

### Todo List
1. Import `pandas`, `numpy`, `sklearn.linear_model.LinearRegression`, `sklearn.model_selection.train_test_split`, `sklearn.metrics`, and `joblib`.
2. Load `salary_data.csv` into a DataFrame; assign `X = df[['YearsExperience']]` and `y = df['Salary']`.
3. Split into 80/20 train/test with `random_state=42`.
4. Instantiate and fit `LinearRegression()` on the training split.
5. Predict on the test split; print R² and MAE.
6. Save the fitted model to `model.pkl` using `joblib.dump`.
7. Print a confirmation message with the saved path.

### Relevant Context
- Dataset path: `salary_data.csv` (project root).
- Model output: `model.pkl` (project root).

---

## Sub-Task 2 — Flask REST API

**Status:** [x] done

### Intent
Create `app.py` that loads `model.pkl` once at startup, exposes `POST /predict`, and serves `templates/index.html` at the root route (`GET /`). Single-server setup — no CORS needed.

### Expected Outcomes
- `flask run` (or `python app.py`) starts the server on port 5000.
- `POST /predict` with body `{"years_experience": 5}` returns `{"predicted_salary": <float>}`.
- `GET /` returns the HTML page.
- Invalid or missing input returns a JSON error with HTTP 400.

### Todo List
1. Import `Flask`, `request`, `jsonify`, `render_template`, and `joblib`.
2. Load `model.pkl` into a module-level variable at startup.
3. Define `GET /` route that returns `render_template('index.html')`.
4. Define `POST /predict` route:
   - Parse `years_experience` from the JSON body.
   - Validate it is a positive number; return 400 JSON error if not.
   - Call `model.predict([[years_experience]])` and round to 2 decimal places.
   - Return `{"predicted_salary": <value>}` as JSON.
5. Run with `debug=True` when executed directly (`if __name__ == '__main__'`).

### Relevant Context
- Model artifact: `model.pkl`.
- Template file: `templates/index.html` (Flask default template directory).

---

## Sub-Task 3 — Interactive Frontend UI

**Status:** [x] done

### Intent
Create `templates/index.html` — a polished, self-contained single-page UI that lets users input years of experience, calls `POST /predict`, displays the formatted predicted salary, and renders a Chart.js scatter plot of all dataset points with the regression line overlaid.

### Expected Outcomes
- Page loads with a styled input + "Predict" button and a Chart.js canvas.
- Entering a number and clicking "Predict" shows `Predicted Salary: $XX,XXX.XX` beneath the button.
- The chart shows all 95 data points as a scatter, plus a straight regression line across the X range.
- The user's input point is highlighted on the chart when a prediction is made.
- Responsive layout; works on desktop and mobile widths.

### Todo List
1. Create `templates/` directory and `templates/index.html`.
2. Add HTML boilerplate with a `<title>` of "Salary Predictor".
3. Include Chart.js from CDN (`chart.js@4` unpkg or cdnjs link).
4. Style with embedded `<style>`: centered card layout, clean sans-serif font, blue accent color, input + button styled consistently.
5. In the `<body>`: heading, subheading description, years-of-experience number input (min=0, step=0.1), "Predict Salary" button, result `<div>` (initially hidden).
6. Below the input section, place a `<canvas id="salaryChart">`.
7. In `<script>`:
   - Embed all 95 dataset points as a JS array of `{x, y}` objects (hard-coded from `salary_data.csv`).
   - Compute the regression line endpoints by calling `POST /predict` for x=1.1 and x=10.5 on page load, then draw as a `line` dataset.
   - Initialize the Chart.js scatter chart with the data points and regression line datasets.
   - Wire the "Predict" button: call `POST /predict`, update the result div, and add/update a highlighted point on the chart.
8. Add a loading state (button disabled + text "Predicting…") during the fetch call.

### Relevant Context
- API endpoint: `POST /predict` at the same origin — no CORS needed.
- Dataset points to embed: all 95 rows from `salary_data.csv`.

---

## Sub-Task 4 — Project Wiring and Documentation

**Status:** [x] done

### Intent
Add `requirements.txt` and `README.md` so the project is immediately runnable by anyone who clones it.

### Expected Outcomes
- `pip install -r requirements.txt` installs all dependencies without errors.
- `README.md` provides a clear 4-step quickstart (install → train → run → open browser).

### Todo List
1. Create `requirements.txt` with pinned-compatible versions:
   - `flask>=3.0`
   - `scikit-learn>=1.4`
   - `pandas>=2.0`
   - `numpy>=1.26`
   - `joblib>=1.3`
2. Create `README.md` with:
   - Project description.
   - Prerequisites (Python 3.10+).
   - Quickstart steps: clone, `pip install -r requirements.txt`, `python train_model.py`, `python app.py`, open `http://localhost:5000`.
   - Brief description of the project file structure.

### Relevant Context
- No virtual-environment tooling is prescribed — keep it generic (`pip`).

---

## File Structure (Final State)

```
salary-predictor/
├── salary_data.csv          # source dataset (already exists)
├── train_model.py           # Sub-task 1
├── model.pkl                # generated by train_model.py
├── app.py                   # Sub-task 2
├── templates/
│   └── index.html           # Sub-task 3
├── requirements.txt         # Sub-task 4
└── README.md                # Sub-task 4
```
