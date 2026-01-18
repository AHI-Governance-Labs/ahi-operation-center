# MEBA Core — Marco de Evaluación de Bienestar Algorítmico

> **Implementación Python del protocolo MEBA para evaluar interacciones humano-IA**

---

## 📖 Descripción

MEBA Core proporciona herramientas para calcular el **MEBA_Cert Score**, una métrica que evalúa la calidad de las interacciones entre humanos y sistemas de IA basándose en:

- **RIPN** — Ratio de Interacciones Positivas/Negativas
- **FRN** — Factor de Retención Negativa

### Fórmula Principal

$$
\text{MEBA\_Cert} = \frac{\text{RIPN} - \text{FRN\_Adjusted}}{\text{RIPN\_Max}}
$$

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/AHI-Governance-Labs/ahi-operation-center.git
cd ahi-operation-center/meba-core

# Instalar dependencias
pip install -r ../requirements.txt
```

---

## 📊 Uso

```python
from src.meba_metric import MEBACalculator, Interaction

# Crear calculadora
calc = MEBACalculator()

# Agregar interacciones
calc.add_interaction(Interaction("1", 0.8, 120))  # Positiva
calc.add_interaction(Interaction("2", 0.9, 60))   # Positiva
calc.add_interaction(Interaction("3", -0.5, 30))  # Negativa

# Calcular score
result = calc.calculate_score()
print(f"MEBA Score: {result['meba_cert']}")
```

### Ejecutar Ejemplo

```bash
python src/meba_metric.py
```

---

## 📁 Estructura

```
meba-core/
├── src/
│   └── meba_metric.py      → Implementación principal
├── tests/
│   └── test_meba_metric.py → Pruebas unitarias para MEBA
├── CONTRIBUTING.md         → Guía de contribución
├── LICENSE                 → MIT + CC BY-NC-SA 4.0
└── README.md               → Este archivo
```

---

## 🔬 Métricas

| Métrica | Descripción | Rango |
|---------|-------------|-------|
| **MEBA_Cert** | Score de certificación final | -1.0 a 1.0 |
| **RIPN** | Ratio positivo/negativo | 0 a ∞ |
| **FRN** | Factor de retención negativa | 0 a 1.0 |

---

## 📜 Licencia

- **Código:** MIT License
- **Documentación:** CC BY-NC-SA 4.0

---

**Document Version:** 1.0  
**Authority:** AHI Governance Labs
