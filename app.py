# ============================================================
#  Student Performance Predictor — Flask Application
#  Run:  python app.py
#  API:  POST /predict  { study_hours, attendance, previous_marks }
# ============================================================

import os
import numpy as np
import joblib
from flask import Flask, request, jsonify, render_template

# ── App setup ────────────────────────────────────────────────
app = Flask(__name__)

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "model", "student_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

# ── Load model & scaler once at startup ──────────────────────
try:
    model  = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and scaler loaded successfully.")
except FileNotFoundError:
    raise RuntimeError(
        "❌ Model files not found. Please run  python train_model.py  first."
    )


# ── Helper: grade label ──────────────────────────────────────
def get_grade(score: float) -> dict:
    if score >= 90:
        return {"grade": "A+", "label": "Outstanding",  "color": "#00e676"}
    elif score >= 80:
        return {"grade": "A",  "label": "Excellent",    "color": "#64dd17"}
    elif score >= 70:
        return {"grade": "B",  "label": "Good",         "color": "#ffd600"}
    elif score >= 60:
        return {"grade": "C",  "label": "Average",      "color": "#ff9100"}
    elif score >= 50:
        return {"grade": "D",  "label": "Below Average","color": "#ff3d00"}
    else:
        return {"grade": "F",  "label": "Needs Improvement", "color": "#f50057"}


# ── Routes ───────────────────────────────────────────────────
@app.route("/")
def index():
    """Serve the main prediction page."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts JSON: { "study_hours": int, "attendance": int, "previous_marks": int }
    Returns JSON: { "predicted_marks": float, "grade": str, "label": str, "color": str }
    """
    try:
        data = request.get_json(force=True)

        study_hours    = float(data["study_hours"])
        attendance     = float(data["attendance"])
        previous_marks = float(data["previous_marks"])

        # Input validation
        errors = []
        if not (0 <= study_hours <= 24):
            errors.append("study_hours must be between 0 and 24.")
        if not (0 <= attendance <= 100):
            errors.append("attendance must be between 0 and 100.")
        if not (0 <= previous_marks <= 100):
            errors.append("previous_marks must be between 0 and 100.")
        if errors:
            return jsonify({"error": " | ".join(errors)}), 400

        features = np.array([[study_hours, attendance, previous_marks]])
        features_scaled = scaler.transform(features)
        prediction = float(model.predict(features_scaled)[0])
        prediction = round(min(max(prediction, 0), 100), 2)   # clamp to [0, 100]

        grade_info = get_grade(prediction)

        return jsonify({
            "predicted_marks": prediction,
            "grade":  grade_info["grade"],
            "label":  grade_info["label"],
            "color":  grade_info["color"],
            "inputs": {
                "study_hours":    study_hours,
                "attendance":     attendance,
                "previous_marks": previous_marks,
            }
        })

    except (KeyError, ValueError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400
    except Exception as exc:
        return jsonify({"error": f"Prediction failed: {exc}"}), 500


@app.route("/health")
def health():
    """Health-check endpoint."""
    return jsonify({"status": "ok", "model": "LinearRegression", "version": "1.0.0"})


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    print(f"\n🎓 Student Performance Predictor running on http://127.0.0.1:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)