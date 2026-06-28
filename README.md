# Student_performance_predicter
Machine Learning project to predict student marks
# 🎓 Student Performance Predictor

A professional machine-learning web application that predicts a student's **final exam marks** based on study habits and past performance — built with **Flask + Scikit-learn**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=flat-square&logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📁 Project Structure

```
STUDENT_PERFORMANCE_PREDICTER/
├── app.py                  # Flask application (routes + prediction API)
├── train_model.py          # Model training script
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── dataset/
│   └── student_performance_dataset_100.csv
│
├── model/
│   ├── student_model.pkl   # Trained LinearRegression model (auto-generated)
│   ├── scaler.pkl          # StandardScaler (auto-generated)
│   └── training_report.png # Diagnostic plots (auto-generated)
│
├── templates/
│   └── index.html          # Frontend HTML
│
└── static/
    ├── style.css           # Dark theme stylesheet
    └── script.js           # Frontend JavaScript
```

---

## ✨ Features

- 🤖 **Linear Regression** model trained on 100 student records
- 📊 **3 smart inputs**: Study Hours · Attendance · Previous Marks
- 🎨 **Professional dark-themed UI** with animated gradients
- 🔢 **Animated score ring** with grade (A+ → F) and colour coding
- ✅ Client-side + server-side input validation
- 📈 Training report with Actual vs Predicted & Residual plots
- 🌐 REST API endpoint (`/predict`) — JSON in / JSON out
- 🏥 Health-check endpoint (`/health`)

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/student_performance_predicter.git
cd student_performance_predicter
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Place your dataset
Copy `student_performance_dataset_100.csv` into the `dataset/` folder.

### 5. Train the model
```bash
python train_model.py
```
This generates `model/student_model.pkl`, `model/scaler.pkl`, and a training report plot.

### 6. Run the app
```bash
python app.py
```
Open your browser at **http://127.0.0.1:5000**

---

## 🔌 API Reference

### `POST /predict`
**Request body (JSON)**
```json
{
  "study_hours":    6,
  "attendance":     85,
  "previous_marks": 72
}
```

**Response (JSON)**
```json
{
  "predicted_marks": 81.34,
  "grade":  "A",
  "label":  "Excellent",
  "color":  "#64dd17",
  "inputs": {
    "study_hours": 6,
    "attendance": 85,
    "previous_marks": 72
  }
}
```

### `GET /health`
```json
{ "status": "ok", "model": "LinearRegression", "version": "1.0.0" }
```

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Algorithm | Linear Regression |
| MAE | ~3.5 |
| RMSE | ~4.8 |
| R² Score | ~0.93 |
| Cross-Val R² | ~0.91 ± 0.04 |

---

## 🎨 Grade Scale

| Grade | Range | Label |
|-------|-------|-------|
| A+ | ≥ 90 | Outstanding |
| A  | ≥ 80 | Excellent |
| B  | ≥ 70 | Good |
| C  | ≥ 60 | Average |
| D  | ≥ 50 | Below Average |
| F  | < 50 | Needs Improvement |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Flask 3.1 |
| ML | Scikit-learn (LinearRegression, StandardScaler) |
| Data | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| Frontend | HTML5, CSS3 (custom dark theme), Vanilla JS |
| Deployment | Gunicorn (production WSGI) |

---

## 🌐 Deploy to Render / Railway

Add a `Procfile`:
```
web: gunicorn app:app
```
Set environment variable `PORT` if required by the platform.

---

## 📄 License

MIT © 2026 — feel free to use, modify, and share.