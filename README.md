# EventStreamApp (public)

Pequeño stack de eventos con **Kafka + ZooKeeper + Redis** y 4 servicios:
- **event-generator (API)**: `POST /publish` publica en el tópico `events`.
- **event-consumer**: lee de Kafka y guarda en Redis (`event_log`).
- **event-viewer**: muestra últimos eventos en `/events` (raíz `/` redirige).
- **automatic-generator**: genera eventos cada 2s (con reintentos a Kafka).

## 🚀 Quickstart

```bash
# Levantar todo (compose + override)
docker compose up -d

# Ver estado y puertos
docker compose ps

