from flask import Flask, request, jsonify
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
from datetime import datetime

app = Flask(__name__)

# Intentar conectarse a Kafka con reintentos
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("[INFO] Conectado a Kafka desde event-generator")
        break
    except NoBrokersAvailable:
        print("[WARN] Kafka no disponible, reintentando en 5 segundos...")
        time.sleep(5)

@app.route('/publish', methods=['POST'])
def publish_event():
    data = request.get_json()

    if not data or 'action' not in data:
        return jsonify({"error": "Missing 'action' field"}), 400

    # Generar user automático con timestamp si no viene
    if 'user' not in data:
        now = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
        data['user'] = f"user_{now}"

    data["timestamp"] = datetime.utcnow().isoformat()

    producer.send("events", data)
    producer.flush()

    return jsonify({"status": "event published", "event": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
