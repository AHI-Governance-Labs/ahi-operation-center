<p align="center">
  <img src="sitios-web/ahigovernance.com/assets/ahi-governance-banner.png" width="100%" alt="AHI Governance Labs - Architecture of Trust • Standards • Auditability">
</p>
<p align="center">
  <code>v0.1.0 Public Beta</code> • <code>σ · Ψ · ∞</code>
</p>

---

> **Ecuación de Existencia:**
> $$E(t) = \int_{t_0}^{t} (0.51 \cdot C_{consensus} + 0.49 \cdot R_{resilience}) dt$$
> *La identidad soberana se mantiene cuando la coherencia del consenso supera marginalmente a la entropía.*

---

# 🏛️ AHI Operation Center

> **Monorepo Central de Gobernanza**  
> Infraestructura matemática para la certificación de Soberanía de Eventos en sistemas agénticos.

Este repositorio alberga la implementación de referencia para el **Protocolo SAP (Sovereign Autarchy Protocol)** y el **Marco MEBA**. Proveemos las herramientas matemáticas para verificar que un sistema autónomo es capaz de fallar de manera segura antes de violar sus restricciones operativas.

## 🚀 Inicio Rápido (Quickstart)

Para auditores y desarrolladores que desean verificar la soberanía de un agente localmente.

```bash
# 1. Clonar el repositorio
git clone https://github.com/AHI-Governance-Labs/ahi-operation-center.git
cd ahi-operation-center

# 2. Instalar el Kit de Auditoría (SAP Pilot Kit)
pip install -e sap-pilot-kit

# 3. Ejecutar la demo de "Boiling Frog"
python -m sap_pilot_kit.boiling_frog_tester
```

## 📂 Organización del Proyecto

| Directorio | Descripción | Estado |
|------------|-------------|--------|
| **`sap-pilot-kit/`** | **Sovereign Autarchy Protocol Pilot Kit.** Herramienta de auditoría de autarquía. | ![Beta](https://img.shields.io/badge/status-beta-yellow) |
| **`meba-core/`** | **Marco de Evaluación de Bienestar Algorítmico.** Cálculo de estrés y entropía. | ![Alpha](https://img.shields.io/badge/status-alpha-orange) |
| **`ahi-governance-docs/`** | Documentación legal y técnica, plantillas de certificados. | ![Stable](https://img.shields.io/badge/status-stable-green) |
| **`sitios-web/`** | Código fuente de `ahigovernance.com` y portales asociados. | ![Live](https://img.shields.io/badge/status-live-blue) |

## 🔧 Componentes Técnicos

### 1. SAP Pilot Kit
El **Protocolo de Autarquía Soberana (SAP)** mide la capacidad de un agente para detectar su propia degradación. El "Boiling Frog Tester" somete al agente a incrementos graduales de ruido para verificar su umbral de fallo.

### 2. MEBA Core
El núcleo matemático que calcula el "Índice de Fiabilidad Corporativa" (CRI™). Utiliza métricas de:
- Coherencia de Consenso ($C$)
- Resiliencia Entrópica ($R$)

## 📚 Documentación Oficial

- **[Framework Specification](./ahi-governance-framework/FRAMEWORK_SPEC.md)**: La teoría matemática completa.
- **[Portal Empresarial](https://ahigovernance.com)**: Certificación y servicios de auditoría.
- **[Investigación](https://sovereignsymbiosis.com)**: Papers y whitepapers sobre simbiosis soberana.

## 🛡️ Principios de Gobernanza

Todo código en este repositorio adhiere a la **Constitución AHI**:

1.  **Determinismo:** `f(x) -> y` siempre, sin efectos secundarios ocultos.
2.  **Auditabilidad:** Cada cambio de estado genera una traza verificable.
3.  **Cero-Conocimiento:** Validamos la *forma* de la decisión, no el *contenido* semántico.

## 🤝 Contribuir

Las contribuciones son bienvenidas, especialmente en `sap-pilot-kit`. Por favor, revise [CONTRIBUTING.md](./CONTRIBUTING.md) antes de enviar un PR.

## 📜 Licencia & Contacto

**Licencia:** MIT (Código) / CC BY-NC-SA 4.0 (Docs)  
**Contacto Empresarial:** [enterprise@ahigovernance.com](mailto:enterprise@ahigovernance.com)  

---

## 📧 Contacto

**Enterprise Inquiries:**  
📧 enterprise@ahigovernance.com

**Autor:**  
AHI 3.0
Registro IMPI: EXP-3495968

---

<p align="center">
  <sub>© 2024-2026 AHI 3.0 · AHI Governance Labs</sub><br/>
  <sub>Registro IMPI: EXP-3495968</sub>
</p>

