from kafka import KafkaConsumer
import redis
import json
import time
from kafka.errors import NoBrokersAvailable
from concurrent.futures import ThreadPoolExecutor
from dateutil import parser

# Conectarse a Kafka
while True:
    try:
        consumer = KafkaConsumer(
            "events",
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='event-consumer-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        print("[INFO] Conectado a Kafka y escuchando...")
        break
    except NoBrokersAvailable:
        print("[WARN] Kafka no disponible, reintentando en 5s...")
        time.sleep(5)

# Conexión con Redis
r = redis.Redis(host='redis', port=6379)

# Pool de hilos para procesamiento paralelo
pool = ThreadPoolExecutor(max_workers=4)
contador = 0

def guardar_en_redis(event):
    user = event.get("user", "unknown")
    timestamp = event.get("timestamp", time.time())

    try:
        # Convertir ISO 8601 a timestamp numérico si es string
        if isinstance(timestamp, str):
            timestamp = parser.isoparse(timestamp).timestamp()

        # Guardar por usuario
        r.set(f"event:{user}", json.dumps(event))

        # Guardar en conjunto ordenado para historial
        r.zadd("event_log", {json.dumps(event): float(timestamp)})

        print(f"[INFO] Evento guardado: event:{user}")
        return f"{user} OK"
    except redis.exceptions.RedisError as e:
        print(f"[ERROR] Redis fallo para {user}: {e}")
        return f"{user} ERROR: {e}"

# Bucle principal
for msg in consumer:
    event = msg.value
    pool.submit(guardar_en_redis, event)

    contador += 1
    if contador % 10 == 0:
        print(f"[INFO] Procesados {contador} eventos")
