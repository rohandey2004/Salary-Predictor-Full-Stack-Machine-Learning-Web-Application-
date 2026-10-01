"""
train_model.py
--------------
Loads salary_data.csv, trains a Linear Regression model, evaluates it,
and saves the fitted model to model.pkl using joblib.

Usage:
    python train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# ── 1. Load data ──────────────────────────────────────────────────────────────
df = pd.read_csv("salary_data.csv")

X = df[["YearsExperience"]]
y = df["Salary"]

print(f"Dataset loaded: {len(df)} rows")
print(f"YearsExperience range: {X['YearsExperience'].min()} – {X['YearsExperience'].max()}")
print(f"Salary range: ${y.min():,.0f} – ${y.max():,.0f}")
print()

# ── 2. Train / test split (80 / 20) ──────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples : {len(X_train)}")
print(f"Test samples     : {len(X_test)}")
print()

# ── 3. Train model ────────────────────────────────────────────────────────────
model = LinearRegression()
model.fit(X_train, y_train)

print(f"Model trained:")
print(f"  Coefficient (slope)  : {model.coef_[0]:,.2f}")
print(f"  Intercept            : {model.intercept_:,.2f}")
print()

# ── 4. Evaluate ───────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
r2  = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"Evaluation on test set:")
print(f"  R² Score             : {r2:.4f}")
print(f"  Mean Absolute Error  : ${mae:,.2f}")
print()

# ── 5. Save model ─────────────────────────────────────────────────────────────
model_path = "model.pkl"
joblib.dump(model, model_path)
print(f"Model saved -> {model_path}")
