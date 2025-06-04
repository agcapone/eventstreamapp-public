# Makefile para controlar el automatic-generator

start-generator:
	docker compose up -d automatic-generator
	@echo "automatic-generator iniciado"

stop-generator:
	docker stop eventstreamapp-automatic-generator-1
	@echo "automatic-generator detenido"

restart-generator: stop-generator start-generator

logs-generator:
	docker logs -f eventstreamapp-automatic-generator-1

status:
	docker ps | grep automatic-generator || echo "❌ automatic-generator no está corriendo"
