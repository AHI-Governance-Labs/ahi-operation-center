<p align="center">
  <strong>AHI GOVERNANCE LABS</strong><br/>
  <em>Autonomous Hierarchy of Intelligence — Operation Center v2</em>
</p>

<p align="center">
  <code>σ · Ψ · ∞</code>
</p>

---

# 🏛️ AHI Operation Center v2

> **Arquitectura Evolucionada del Monorepo Central de Gobernanza**

Esta versión representa una evolución arquitectónica del repositorio original, optimizada para escalabilidad, mantenibilidad y desarrollo colaborativo.

---

## 📂 Estructura del Repositorio

```
ahi-operation-center-v2/
│
├── packages/                   # Paquetes instalables (pip install -e)
│   ├── meba-core/             # Marco de Evaluación de Bienestar Algorítmico
│   ├── sap-pilot-kit/         # Sovereign Autarchy Protocol - Kit de Auditoría
│   └── ahi-cli/               # CLI Unificada
│
├── apps/                       # Aplicaciones desplegables
│   ├── api-gateway/           # REST API (FastAPI)
│   └── web-governance/        # Sitio web ahigovernance.com
│
├── docs/                       # Documentación unificada
│   ├── governance/            # Biblioteca normativa (EN/ES)
│   ├── api/                   # OpenAPI specs
│   ├── FRAMEWORK_SPEC.md      # Especificación canónica
│   └── README.md              # Índice de documentación
│
├── research/                   # Scripts de investigación
│   ├── simulations/           # Simulaciones Alpha
│   ├── analysis/              # Análisis de datos
│   └── experiments/           # Experimentos
│
├── infrastructure/             # Infraestructura como código
│   └── docker/                # Dockerfile + docker-compose
│
├── pyproject.toml             # Configuración principal (workspaces)
└── README.md                  # Este archivo
```

---

## 🚀 Quick Start

### Instalación de Desarrollo

```bash
# Clonar e instalar
git clone https://github.com/AHI-Governance-Labs/ahi-operation-center.git
cd ahi-operation-center/ahi-operation-center-v2

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar en modo desarrollo
pip install -e ".[dev]"
pip install -e packages/meba-core
pip install -e packages/sap-pilot-kit
pip install -e packages/ahi-cli
```

### Usando la CLI

```bash
# Ver información
ahi info

# Calcular MEBA score
ahi meba calculate

# Ejecutar SAP test
ahi sap test --artifact-id MI-SISTEMA-001

# Ver ayuda
ahi --help
```

### Docker

```bash
cd infrastructure/docker

# Desarrollo
docker-compose up dev

# API Gateway
docker-compose up api

# Tests
docker-compose run test
```

---

## 🔧 Componentes

### 📊 MEBA Core
Marco de Evaluación de Bienestar Algorítmico.

```python
from meba_metric import MEBACalculator, Interaction

calc = MEBACalculator()
calc.add_interaction(Interaction("1", 0.8, 120))
result = calc.calculate_score()
```

### 🔒 SAP Pilot Kit
Kit de auditoría del Sovereign Autarchy Protocol.

```python
from ice_w_logger import ICEWLogger
logger = ICEWLogger("MI-SISTEMA", "sha256_hash")
```

### 🌐 API Gateway
REST API para certificaciones.

```bash
# Iniciar API
cd apps/api-gateway
uvicorn src.main:app --reload

# Endpoints:
# POST /api/v1/meba/calculate
# POST /api/v1/sap/test
# GET  /api/v1/certificates/{id}
```

---

## 📈 Mejoras vs v1

| Aspecto | v1 (Original) | v2 (Evolucionado) |
|---------|--------------|-------------------|
| **Estructura** | Archivos en raíz | packages/, apps/, docs/ |
| **CLI** | Scripts separados | CLI unificada (`ahi`) |
| **API** | No existía | FastAPI Gateway |
| **Docker** | No existía | Multi-stage builds |
| **Paquetes** | Monolítico | Instalables por separado |
| **Tests** | Por módulo | Centralizado con coverage |

---

## 🧪 Tests

```bash
# Todos los tests
pytest packages/*/tests -v

# Con coverage
pytest --cov=packages --cov-report=html

# Solo MEBA
pytest packages/meba-core/tests -v
```

---

## 📜 Licencia

- **Código:** MIT License
- **Documentación:** CC BY-NC-SA 4.0

---

<p align="center">
  <sub>© 2024-2026 Luis Carlos Villarreal Elizondo · AHI Governance Labs</sub><br/>
  <sub><strong>σ</strong> Preserving Structural Coherence · <strong>Ψ</strong> Ontological Integrity</sub>
</p>
