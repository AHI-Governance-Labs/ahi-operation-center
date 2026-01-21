# AHI Governance Labs — SAP Pilot Kit

---

## 1. Overview

The SAP Pilot Kit provides a **deterministic auditing mechanism** (Sovereign Autarchy Protocol) for AI systems to enforce internal stability limits during execution.

> It includes tools to simulate event-level failures and verify that the system self-invalidates when coherence thresholds are breached.

---

## 2. Repository Structure

| File | Description |
|------|-------------|
| `src/boiling_frog_tester.py` | Stress-test that gradually increases ambiguity |
| `src/ice_w_logger.py` | Logging utilities for event-level data |
| `certificate_template.md` | Template for audit certificates (technical only) |

---

## 3. Installation

```bash
# Clone from the monorepo root
git clone https://github.com/AHI-Governance-Labs/ahi-operation-center.git
cd ahi-operation-center/sap-pilot-kit
pip install .
```

---

## 4. Usage

```bash
python src/boiling_frog_tester.py
```

### Available Commands

| Command | Description |
|---------|-------------|
| `--artifact-id` | Specify the artifact ID to test |
| `--verbose` | Enable detailed logging output |
| `--output` | Specify output file for telemetry |

---

## 5. Core Principles

All tooling in this kit operates under these non-negotiable principles:

| Principle | Description |
|-----------|-------------|
| **Determinism** | State transitions are reproducible |
| **Auditability** | All events are logged and verifiable |
| **Zero-Knowledge** | No semantic content is accessed or stored |
| **Fail-Safe** | Fast failure over graceful degradation |

```
This is governance infrastructure, not a general-purpose AI toolkit.
```

---

## 6. Governance

This repository is governed by the **AHI Governance Framework**.

See the canonical specification at:

- [FRAMEWORK_SPEC.md](https://github.com/AHI-Governance-Labs/ahi-governance-framework/blob/main/FRAMEWORK_SPEC.md)

---

## 7. Related Documents

| Document | Description |
|----------|-------------|
| `CONTRIBUTING.md` | Contribution guidelines |
| `CODE_OF_CONDUCT.md` | Behavioral standards |
| `SECURITY.md` | Vulnerability disclosure policy |
| `LICENSE` | MIT + CC BY-NC-SA 4.0 |

---

**Document Version:** 1.0  
**Last Updated:** 2025-01  
**Authority:** AHI Governance Labs
