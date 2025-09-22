#prueba de cambio 1
import os
from itertools import cycle
CLIENTS = os.getenv("CLIENT_IDS", "client1,client2,client3,client4").split(",")
CLIENTS = [c.strip() for c in CLIENTS if c.strip()]
client_iter = cycle(CLIENTS)
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaTimeoutError, KafkaError
import json
import time
from datetime import datetime
import random

def connect_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("[INFO] Conectado a Kafka (automatic-generator)")
            return producer
        except NoBrokersAvailable:
            print("[WARN] Kafka no disponible, reintentando en 5 segundos...")
            time.sleep(5)

def main():
    actions = ['login', 'purchase', 'logout']
    producer = connect_producer()
    print("[INFO] Iniciando generación automática de eventos cada 2 segundos...")

    while True:
        event = {
           "user": next(client_iter),     # <— antes era user_auto_...
           "action": random.choice(actions),
           "timestamp": datetime.utcnow().isoformat()
}

        try:
            producer.send("events", event)
            producer.flush()
            print(f"[GENERADO] {event}")
        except (KafkaTimeoutError, KafkaError) as e:
            print(f"[ERROR] Kafka error: {e}. Reintentando conexión...")
            producer = connect_producer()
            continue

        time.sleep(2)

if __name__ == "__main__":
    main()
