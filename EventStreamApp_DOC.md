# Documentación del Proyecto EventStreamApp


# Documentación del Proyecto: EventStreamApp

## Objetivo
EventStreamApp es una arquitectura ligera diseñada para generar, transmitir, procesar y almacenar eventos de forma asincrónica utilizando tecnologías modernas como Kafka, Redis y Docker.

## Componentes

### 1. **event-generator**
Una API REST creada con Flask que recibe eventos manuales a través del endpoint `/publish`. También genera un `user_id` automático si no se especifica y le añade un timestamp.

- Publica los eventos al topic `events` de Kafka.

### 2. **automatic-generator**
Una aplicación que genera eventos de forma automática cada 2 segundos, sin necesidad de interacción humana.
- Utiliza el mismo topic `events` para enviar datos a Kafka.
- Corre en segundo plano y puede ser detenida mediante `docker stop`.

### 3. **event-consumer**
Escucha el topic `events` en Kafka y guarda los eventos recibidos en Redis de dos formas:
- Como claves individuales por usuario (`event:<user_id>`)
- Como historial ordenado (`event_log`), usando `zadd` y el timestamp como score.

### 4. **event-viewer**
Una interfaz básica que permite visualizar los últimos eventos almacenados en Redis accediendo al puerto 5000.

## Infraestructura

Todo el sistema está orquestado con `docker-compose` y compuesto por:
- Kafka + Zookeeper
- Redis
- 4 microservicios Python (generator, automatic-generator, consumer, viewer)

## Flujo del Evento

1. El evento se genera manualmente (`curl`) o automáticamente.
2. Kafka recibe el evento y lo propaga.
3. El consumer escucha el topic y lo guarda en Redis.
4. Viewer permite visualizar los últimos eventos.

## Utilidad

Este entorno es útil para pruebas de arquitecturas basadas en eventos, benchmarking de rendimiento, y como base para proyectos distribuidos y sistemas en tiempo real.



---


# 📘 Resumen de Comandos - Proyecto EventStreamApp

## ⚙️ Docker y Docker Compose

| Comando | Propósito |
|--------|-----------|
| `docker compose up -d` | Levanta todos los servicios definidos en `docker-compose.yml`. |
| `docker compose down` | Detiene y elimina todos los contenedores, redes y dependencias. |
| `docker compose build` | Reconstruye las imágenes Docker. |
| `docker ps` | Muestra los contenedores en ejecución. |
| `docker ps -a` | Muestra todos los contenedores, incluso los detenidos. |
| `docker logs <nombre>` | Muestra logs de un contenedor. |
| `docker exec -it <nombre> bash` | Abre una consola dentro de un contenedor. |
| `docker stop <nombre>` | Detiene un contenedor. |
| `docker rm <nombre>` | Elimina un contenedor detenido. |
| `docker container prune` | Elimina contenedores detenidos. |
| `docker image prune` | Elimina imágenes colgantes no utilizadas. |

## 🐍 Aplicaciones del Proyecto

| Componente | Propósito |
|------------|-----------|
| `event-generator` | API Flask que envía eventos manualmente a Kafka vía HTTP. |
| `automatic-generator` | Script que genera eventos automáticos cada 2 segundos. |
| `event-consumer` | Escucha Kafka y guarda eventos en Redis. |
| `event-viewer` | API Flask para consultar eventos desde Redis (HTML/JSON). |

## 📦 Redis CLI

| Comando | Propósito |
|---------|-----------|
| `docker exec -it eventstreamapp-redis-1 redis-cli` | Accede a Redis CLI. |
| `KEYS *` | Lista todas las claves. |
| `GET event:<user>` | Consulta un evento por usuario. |
| `ZREVRANGE event_log 0 0` | Último evento registrado. |
| `ZREVRANGE event_log 0 9` | Últimos 10 eventos. |

## 🛠️ Makefile Personalizado

| Comando `make` | Propósito |
|----------------|-----------|
| `make start-generator` | Inicia el generador automático. |
| `make stop-generator` | Detiene el generador automático. |
| `make restart-generator` | Reinicia el generador automático. |
| `make logs-generator` | Muestra logs en vivo del generador automático. |
| `make status` | Muestra si el generador automático está activo. |

## 🧪 curl para Pruebas

| Comando | Propósito |
|---------|-----------|
| `curl -X POST http://localhost:8080/publish -H "Content-Type: application/json" -d '{"action":"test"}'` | Publica un evento manualmente. |
| `curl http://localhost:5000/events` | Consulta eventos en formato HTML. |
| `curl -H "Accept: application/json" http://localhost:5000/events` | Consulta eventos en formato JSON. |


---


## Comandos útiles de Kafka

- **Ver mensajes del topic `events` desde el principio**:
  ```bash
  kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic events --from-beginning
  ```

Este comando permite visualizar todos los eventos publicados en el topic `events`, desde el inicio.

---

## Componentes de Kafka usados en este proyecto

- **Zookeeper**: coordina los brokers de Kafka y gestiona la configuración del clúster.
- **Kafka Broker**: almacena los mensajes publicados y permite que los consumidores los lean.
- **Topic** (`events`): canal lógico donde se publican los mensajes desde los generadores y del que leen los consumidores.
- **Kafka Producer**: componente usado en los servicios `event-generator` y `automatic-generator` para enviar eventos al topic.
- **Kafka Consumer**: utilizado en el servicio `event-consumer` para suscribirse al topic `events` y procesar los mensajes.

---

## Funcionamiento resumido

1. Los generadores (manual y automático) producen eventos en formato JSON y los publican en Kafka.
2. Kafka los almacena en el topic `events`.
3. El consumidor lee estos eventos y los guarda en Redis:
   - Como clave individual por usuario.
   - En un conjunto ordenado llamado `event_log`.
4. Un visor permite consultar estos eventos a través de una API web.

Este flujo permite simular un sistema de eventos en tiempo real con almacenamiento y visualización.

## 🛠 Cómo lanzar y detener el proyecto desde cero

### Estructura de directorios esperada:
```
eventstreamapp/
├── docker-compose.yml
├── Makefile
├── event-generator/
│   ├── Dockerfile
│   └── main.py
├── event-consumer/
│   ├── Dockerfile
│   └── main.py
├── automatic-generator/
│   ├── Dockerfile
│   └── main.py
├── event-viewer/
│   ├── Dockerfile
│   └── main.py
```

### 🔼 Para lanzar el proyecto desde cero:
1. Asegúrate de estar en la raíz del proyecto: `cd /home/alejandro/eventstreamapp`
2. Ejecuta:
```bash
docker compose build
docker compose up -d
```
3. Verifica que todos los contenedores estén corriendo:
```bash
docker ps
```

### 🔽 Para detener completamente el proyecto y liberar recursos:
```bash
docker compose down --volumes --remove-orphans
docker system prune -af --volumes  # ⚠️ Esto elimina todos los contenedores e imágenes no utilizadas
```

> 📌 Asegúrate de que tus datos importantes en Redis u otros contenedores estén respaldados si ejecutas `prune`.