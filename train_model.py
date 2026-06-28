# ============================================================
#  Student Performance Predictor — Model Training Script
#  Features: study_hours | attendance | previous_marks
#  Target  : final_marks
# ============================================================

import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ── Paths ────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_PATH   = os.path.join(BASE_DIR, "dataset", "student_performance_dataset_100.csv")
MODEL_DIR   = os.path.join(BASE_DIR, "model")
MODEL_PATH  = os.path.join(MODEL_DIR, "student_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
os.makedirs(MODEL_DIR, exist_ok=True)

# ── Load & clean ─────────────────────────────────────────────
print("📂 Loading dataset …")
df = pd.read_csv(DATA_PATH)
df = df[["study_hours", "attendance", "previous_marks", "final_marks"]].dropna()
print(f"   ✅ {len(df)} records loaded — columns: {list(df.columns)}")

# ── Features / target ────────────────────────────────────────
FEATURES = ["study_hours", "attendance", "previous_marks"]
TARGET   = "final_marks"

X = df[FEATURES].values
y = df[TARGET].values

# ── Train / test split ───────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# ── Scale ────────────────────────────────────────────────────
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# ── Train ────────────────────────────────────────────────────
print("\n🚀 Training Linear Regression model …")
model = LinearRegression()
model.fit(X_train, y_train)

# ── Evaluate ─────────────────────────────────────────────────
y_pred = model.predict(X_test)
mae    = mean_absolute_error(y_test, y_pred)
rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
r2     = r2_score(y_test, y_pred)
cv     = cross_val_score(model, scaler.transform(X), y, cv=5, scoring="r2")

print("\n📊 Model Performance")
print(f"   MAE  : {mae:.2f}")
print(f"   RMSE : {rmse:.2f}")
print(f"   R²   : {r2:.4f}")
print(f"   CV R²: {cv.mean():.4f} ± {cv.std():.4f}")

# ── Coefficients ─────────────────────────────────────────────
print("\n🔍 Feature Coefficients")
for feat, coef in zip(FEATURES, model.coef_):
    print(f"   {feat:>20s} : {coef:+.4f}")
print(f"   {'intercept':>20s} : {model.intercept_:+.4f}")

# ── Save ─────────────────────────────────────────────────────
joblib.dump(model,  MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
print(f"\n✅ Model  saved → {MODEL_PATH}")
print(f"✅ Scaler saved → {SCALER_PATH}")

# ── Quick diagnostic plot ─────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Student Performance Predictor — Training Report", fontsize=13, fontweight="bold")

# Actual vs Predicted
axes[0].scatter(y_test, y_pred, color="#4f86f7", edgecolors="white", linewidth=0.5, alpha=0.85, s=60)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", linewidth=1.5)
axes[0].set_xlabel("Actual Marks")
axes[0].set_ylabel("Predicted Marks")
axes[0].set_title(f"Actual vs Predicted  (R²={r2:.3f})")

# Residuals
residuals = y_test - y_pred
axes[1].hist(residuals, bins=10, color="#7ec8a4", edgecolor="white")
axes[1].axvline(0, color="red", linestyle="--", linewidth=1.5)
axes[1].set_xlabel("Residual (Actual − Predicted)")
axes[1].set_ylabel("Count")
axes[1].set_title("Residual Distribution")

plt.tight_layout()
plot_path = os.path.join(MODEL_DIR, "training_report.png")
plt.savefig(plot_path, dpi=150)
print(f"📈 Training plot saved → {plot_path}")
plt.show()