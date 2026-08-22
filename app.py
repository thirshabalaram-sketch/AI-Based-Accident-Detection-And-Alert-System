from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from datetime import datetime
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, TWILIO_TO_NUMBER

app = Flask(__name__)
model = joblib.load('model/severity_model.pkl')
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# In-memory event log (resets when server restarts)
events = []

def send_alert_sms(severity_label, lat, lon):
    message_body = f"🚨 Accident Detected! Severity: {severity_label}. Location: https://maps.google.com/?q={lat},{lon}"
    message = twilio_client.messages.create(
        body=message_body,
        from_=TWILIO_FROM_NUMBER,
        to=TWILIO_TO_NUMBER
    )
    print(f"SMS sent, SID: {message.sid}")
    return message.sid

@app.route('/', methods=['GET'])
def home():
    return "Accident Detection Server is running. Visit /dashboard to view the control room."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    required_fields = ['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'speed']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    features = np.array([[
        data['accel_x'], data['accel_y'], data['accel_z'],
        data['gyro_x'], data['gyro_y'], data['gyro_z'],
        data['speed']
    ]])

    severity = int(model.predict(features)[0])
    severity_labels = {0: 'Normal', 1: 'Moderate Accident', 2: 'Severe Accident'}
    css_classes = {0: 'normal', 1: 'moderate', 2: 'severe'}
    label = severity_labels[severity]

    lat = data.get('lat', 8.7139)
    lon = data.get('lon', 77.7567)

    result = {
        'severity': severity,
        'label': label,
        'alert_triggered': severity >= 1
    }

    if severity >= 1:
        sms_sid = send_alert_sms(label, lat, lon)
        result['sms_sid'] = sms_sid

    # Log this event for the dashboard
    events.insert(0, {
        'label': label,
        'css_class': css_classes[severity],
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'speed': round(data['speed'], 1),
        'lat': lat,
        'lon': lon
    })

    print(f"Prediction: {result}")
    return jsonify(result)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    severe_count = sum(1 for e in events if e['css_class'] == 'severe')
    moderate_count = sum(1 for e in events if e['css_class'] == 'moderate')
    return render_template('dashboard.html', events=events[:20], total=len(events),
                            severe_count=severe_count, moderate_count=moderate_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)