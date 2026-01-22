# AHI API Gateway

REST API para servicios de certificación de gobernanza.

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/meba/calculate` | Calcular score MEBA |
| POST | `/api/v1/sap/test` | Ejecutar test SAP |
| GET | `/api/v1/certificates/{id}` | Obtener certificado |

## Ejecución

```bash
# Desarrollo
uvicorn src.main:app --reload

# Producción
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Docker
docker-compose up api
```

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
