"""
Simulated IoT Sensor Data Generator
------------------------------------
Mimics an accelerometer + gyroscope + GPS speed sensor (e.g. MPU6050) sending
live readings to the Flask /predict endpoint, exactly like a real ESP32/Arduino
device would over WiFi or serial.

Use this when physical hardware isn't available for demo/testing purposes.
"""

import requests
import random
import time

SERVER_URL = "http://127.0.0.1:5000/predict"

# Roughly how often (in seconds) to send a reading
SEND_INTERVAL = 3

# 1 in N readings will simulate an accident (tweak to control frequency)
ACCIDENT_CHANCE = 8


def generate_normal_reading():
    """Simulates calm, steady driving."""
    return {
        "accel_x": round(random.uniform(-1.5, 1.5), 2),
        "accel_y": round(random.uniform(-1.5, 1.5), 2),
        "accel_z": round(random.uniform(8.5, 10.5), 2),  # gravity baseline ~9.8
        "gyro_x": round(random.uniform(-1.0, 1.0), 2),
        "gyro_y": round(random.uniform(-1.0, 1.0), 2),
        "gyro_z": round(random.uniform(-1.0, 1.0), 2),
        "speed": round(random.uniform(20, 70), 1),
    }


def generate_accident_reading():
    """Simulates a sudden crash: high acceleration spike, erratic rotation, speed drop."""
    return {
        "accel_x": round(random.uniform(10, 20), 2),
        "accel_y": round(random.uniform(10, 20), 2),
        "accel_z": round(random.uniform(15, 25), 2),
        "gyro_x": round(random.uniform(5, 10), 2),
        "gyro_y": round(random.uniform(5, 10), 2),
        "gyro_z": round(random.uniform(5, 10), 2),
        "speed": round(random.uniform(0, 10), 1),  # sudden stop
    }


def generate_gps():
    """Small random drift around a base location (Tenkasi area coords as example)."""
    base_lat, base_lon = 8.9591, 77.3152
    return {
        "lat": round(base_lat + random.uniform(-0.01, 0.01), 6),
        "lon": round(base_lon + random.uniform(-0.01, 0.01), 6),
    }


def run_simulation():
    print(f"Starting sensor simulation -> POSTing to {SERVER_URL}")
    print(f"Sending a reading every {SEND_INTERVAL}s. Press Ctrl+C to stop.\n")

    reading_count = 0
    while True:
        reading_count += 1
        is_accident = random.randint(1, ACCIDENT_CHANCE) == 1

        data = generate_accident_reading() if is_accident else generate_normal_reading()
        data.update(generate_gps())

        try:
            response = requests.post(SERVER_URL, json=data, timeout=5)
            result = response.json()
            tag = "🚨 ACCIDENT SIM" if is_accident else "normal"
            print(f"[{reading_count}] ({tag}) -> {result}")
        except requests.exceptions.ConnectionError:
            print("Could not reach Flask server. Is app.py running on port 5000?")
            break
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(SEND_INTERVAL)


if __name__ == "__main__":
    run_simulation()