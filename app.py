"""
app.py
------
Flask application that:
  - Loads the trained Linear Regression model (model.pkl) at startup.
  - Serves the frontend UI at GET /.
  - Exposes a prediction endpoint at POST /predict.

Usage:
    python app.py
Then open http://localhost:5000 in your browser.
"""

from flask import Flask, request, jsonify, render_template
import joblib
import os
import warnings

app = Flask(__name__)

# ── Load model once at startup ────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except FileNotFoundError:
    raise RuntimeError(
        "model.pkl not found. Run 'python train_model.py' first."
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the frontend HTML page."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict salary from years of experience.

    Request body (JSON):
        { "years_experience": <float> }

    Response (JSON):
        { "predicted_salary": <float> }
        or
        { "error": "<message>" }  with HTTP 400
    """
    data = request.get_json(silent=True)

    # ── Validate input ────────────────────────────────────────────────────────
    if data is None:
        return jsonify({"error": "Request body must be JSON."}), 400

    years = data.get("years_experience")

    if years is None:
        return jsonify({"error": "Missing field: 'years_experience'."}), 400

    try:
        years = float(years)
    except (TypeError, ValueError):
        return jsonify({"error": "'years_experience' must be a number."}), 400

    if years < 0:
        return jsonify({"error": "'years_experience' must be a non-negative number."}), 400

    # ── Predict ───────────────────────────────────────────────────────────────
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        prediction = model.predict([[years]])[0]
    predicted_salary = round(float(prediction), 2)

    return jsonify({"predicted_salary": predicted_salary})


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
