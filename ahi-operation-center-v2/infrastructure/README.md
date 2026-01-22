# Infrastructure

## Docker

Para desarrollo y despliegue containerizado.

### Comandos Rápidos

```bash
# Desarrollo interactivo
docker-compose up dev

# API Gateway (puerto 8000)
docker-compose up api

# Ejecutar tests
docker-compose run test

# Documentación (puerto 8080)
docker-compose up docs
```

### Build Manual

```bash
# Build para producción
docker build -t ahi-operation-center:latest --target production .

# Build para API
docker build -t ahi-api:latest --target api .
```

## Futuro (Roadmap)

- [ ] Terraform para cloud deployment
- [ ] Kubernetes manifests
- [ ] GitHub Actions avanzados
- [ ] Monitoring con Prometheus
