# Contributing to AHI Operation Center

Welcome to **AHI Governance Labs**. This document outlines the guidelines for contributing to the AHI Operation Center monorepo.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Submission Guidelines](#submission-guidelines)
- [Code Style](#code-style)

---

## Code of Conduct

All contributors must adhere to our [Code of Conduct](./sap-pilot-kit/CODE_OF_CONDUCT.md).

**Key principles:**

| Principle | Description |
|-----------|-------------|
| Technical precision | Communicate with clarity and accuracy |
| Reproducible evidence | Base claims on verifiable data |
| Determinism | Contributions must be reproducible |

---

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- pip

### Clone the Repository

```bash
git clone https://github.com/AHI-Governance-Labs/ahi-operation-center.git
cd ahi-operation-center
```

---

## Development Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
# Test MEBA Core
cd meba-core && python -m pytest tests/ -v

# Test SAP Pilot Kit
cd sap-pilot-kit && python -m pytest tests/ -v
```

### Run Example Scripts

```bash
# MEBA Calculator demo
python meba-core/src/meba_metric.py

# SAP Stress Test demo
python sap-pilot-kit/boiling_frog_tester.py
```

---

## Submission Guidelines

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Make** your changes
4. **Test** your changes: `python -m pytest tests/ -v`
5. **Commit** with clear messages
6. **Push** to your fork
7. **Open** a Pull Request

### Commit Message Format

```
<type>: <short description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

---

## Code Style

### Python

- Follow **PEP 8** style guidelines
- Maximum line length: 120 characters
- Use type hints where applicable
- Include docstrings for all public functions

### Documentation

- Use Markdown for all documentation
- Include code examples where helpful
- Keep documentation in sync with code

---

## Component-Specific Guidelines

### MEBA Core

Contributions to MEBA Core must:
- Include unit tests for new functionality
- Maintain mathematical accuracy of formulas
- Document any changes to metrics

### SAP Pilot Kit

Contributions to SAP Pilot Kit must:
- Pass the Boiling Frog Protocol stress test
- Maintain deterministic state transitions
- Not modify core SAP parameters without approval

---

## Questions?

For questions about contributing:

📧 **enterprise@ahigovernance.com**

---

**Authority:** AHI Governance Labs
