# 🚨 AI-Driven Intelligent Road Accident Detection, Severity Prediction, and Emergency Response System

Using IoT, Edge Computing, and Machine Learning

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black.svg)](https://flask.palletsprojects.com/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)
[![ESP32](https://img.shields.io/badge/Hardware-ESP32-red.svg)](https://www.espressif.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

---

## 📖 Overview

Road traffic accidents remain a leading cause of preventable death, with delayed emergency response often determining survival outcomes during the critical **"golden hour."** This project presents an IoT-enabled accident detection and emergency response system that integrates motion sensors, GPS localization, and GSM-based alerting with a machine learning severity classifier.

The system detects whether an accident has occurred, classifies its severity (**minor/major**), and automatically sends an **SMS alert with live GPS location** to emergency contacts — while logging every event on a **real-time web dashboard**.

---

## ✨ Key Features

- **Multi-sensor fusion** — combines accelerometer, gyroscope, speed, and brake status instead of relying on a single vibration threshold
- **Two-stage ML pipeline** — first detects *"did an accident happen?"*, then classifies *"how severe is it?"*
- **False-positive reduction** — a confirmation window requires multiple consecutive abnormal readings before triggering an alert
- **Automated emergency response** — real SMS alerts via Twilio, including a Google Maps link to the accident location
- **Live dashboard** — real-time event logging and monitoring
- **Edge + Cloud architecture** — ESP32 handles sensing, Flask server handles ML inference
- **Hardware-in-the-loop validation** — tested via Wokwi ESP32 simulation before physical deployment

---

## 🏗️ System Architecture

```
┌──────────────┐     ┌──────────┐     ┌─────────────┐     ┌────────────┐
│  MPU6050     │     │ NEO-6M   │     │ Push Button │     │   ESP32    │
│ (Accel+Gyro) ├────►│   GPS    ├────►│  (Manual)   ├────►│ (Edge Ctrl)│
└──────────────┘     └──────────┘     └─────────────┘     └─────┬──────┘
                                                                  │
                                                          WiFi / GSM
                                                                  │
                                                                  ▼
                                                  ┌───────────────────────┐
                                                  │  Flask REST API Server │
                                                  └───────────┬───────────┘
                                                              │
                                                              ▼
                                                  ┌───────────────────────┐
                                                  │  ML Severity Classifier│
                                                  │  (XGBoost, 95% acc.)   │
                                                  └───────────┬───────────┘
                                                              │
                                                              ▼
                                                  ┌───────────────────────┐
                                                  │  Confirmation Window   │
                                                  │ (filters false alarms) │
                                                  └─────┬─────────────┬───┘
                                                        │             │
                                                        ▼             ▼
                                          ┌──────────────────┐  ┌─────────────┐
                                          │ Twilio SMS Alert  │  │Web Dashboard│
                                          │ (severity + GPS)  │  │(live events)│
                                          └──────────────────┘  └─────────────┘
```

---

## 🧠 Machine Learning Pipeline

| Stage | Model | Input Features | Output |
|---|---|---|---|
| 1. Accident Detection | XGBoost Classifier | speed, acceleration, brake_status, gyro, road_speed_limit | Accident: Yes / No |
| 2. Severity Classification | XGBoost Classifier | Same 5 features (accident rows only) | Severity: Minor / Major |

**Overall accuracy:** 95%
**Training data:** Hybrid dataset — synthetic crash pattern generation combined with empirically collected MPU6050 sensor readings

---

## 🛠️ Tech Stack

**Hardware**
- ESP32 Dev Board
- MPU6050 (Accelerometer + Gyroscope)
- NEO-6M GPS Module
- SIM800L GSM Module
- Push Button, Buzzer
- 18650 Li-ion Battery + TP4056 Charger

**Software**
- Python 3.11
- Flask (REST API backend)
- XGBoost / scikit-learn (ML models)
- Twilio API (SMS alerts)
- Wokwi (hardware simulation)
- ngrok (local server tunneling)

---

## 📁 Project Structure

```
accident-detection-project/
├── data/
│   └── accident_data.csv          # Training dataset (synthetic + real)
├── model/
│   ├── accident_detect_model.pkl  # Stage 1: accident detection model
│   ├── severity_xgb_model.pkl     # Stage 2: severity classification model
│   ├── confusion_matrix.png
│   └── feature_importance.png
├── templates/
│   └── dashboard.html             # Live dashboard UI
├── app.py                         # Flask server (main entry point)
├── config.py                      # API keys and credentials (not committed)
├── generate_dataset.py            # Synthetic dataset generator
├── train_xgb_model.py             # Model training script
├── visualize_results.py           # Generates evaluation charts
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/accident-detection-project.git
cd accident-detection-project
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure credentials
Create a `config.py` file in the project root:
```python
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_FROM_NUMBER = "your_twilio_number"
TWILIO_TO_NUMBER = "your_verified_number"
```

### 5. Generate the dataset and train the models
```bash
python generate_dataset.py
python train_xgb_model.py
```

### 6. Run the server
```bash
python app.py
```
Server runs at `http://127.0.0.1:5000`

### 7. View the dashboard
```
http://127.0.0.1:5000/dashboard
```

---

## 🔌 API Reference

### `POST /predict`

Send sensor readings and receive an accident/severity prediction.

**Request body:**
```json
{
  "speed": 95,
  "acceleration": -6.2,
  "brake_status": 0,
  "gyro": 180,
  "road_speed_limit": 60,
  "lat": 8.7139,
  "lon": 77.7567
}
```

**Response:**
```json
{
  "accident_detected": true,
  "severity": "major",
  "sms_sid": "SMxxxxxxxxxxxxxxxxx"
}
```

---

## 📊 Results

| Metric | Score |
|---|---|
| Overall Accuracy | 95% |
| Normal — Precision / Recall | 1.00 / 1.00 |
| Moderate — Precision / Recall | 0.75 / 0.82 |
| Severe — Precision / Recall | 0.81 / 0.74 |

See `model/confusion_matrix.png` and `model/feature_importance.png` for detailed evaluation visuals.

---

## 🚧 Limitations

- Trained primarily on synthetic and limited real sensor data — not yet validated on large-scale real-world crash telemetry
- No visual/camera confirmation (sensor-only detection)
- Depends on GSM network availability for alert delivery
- Validated via hardware simulation (Wokwi); full field deployment pending

---

## 🔮 Future Work

- [ ] Physical hardware deployment and field testing (2/3/4-wheelers)
- [ ] Camera-based visual confirmation using ESP32-CAM
- [ ] On-device edge inference to reduce latency
- [ ] Larger, real-world multi-vehicle dataset
- [ ] Production-grade SMS gateway (beyond Twilio trial limits)
- [ ] Privacy and anonymity handling for location data

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Department of Electronics and Communication Engineering
- Project Guide: [mrs.m.esakki rani AP/ECE]
- Built as a final-year engineering project

---

## 📬 Contact

[B.THIRSHA]
Final Year ECE Student
Email:thirsha006@gmail.com.com
