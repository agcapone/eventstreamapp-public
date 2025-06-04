from kafka import KafkaProducer
import json
import time
from datetime import datetime
import random

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

actions = ['login', 'purchase', 'logout', 'click', 'view']

print("[INFO] Iniciando generación automática de eventos cada 2 segundos...")

while True:
    action = random.choice(actions)
    timestamp = datetime.utcnow().isoformat()
    user = f"user_auto_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}"

    event = {
        "user": user,
        "action": action,
        "timestamp": timestamp
    }

    producer.send("events", event)
    producer.flush()
    print(f"[GENERADO] {event}")

    time.sleep(2)
