# AHI Governance Labs - Examples

This directory contains runnable examples demonstrating the core components of the AHI Governance Labs toolkit: **SAP Pilot Kit** (Stability/Auditing) and **MEBA Core** (Well-being Metrics).

## Prerequisites

These examples are designed to run from the root of the repository. They automatically handle python path adjustments to import the local `src` packages.

## Scripts

### 1. Basic SAP Audit (`01_basic_sap_audit.py`)
Demonstrates the **Sovereign Autarchy Protocol (SAP)** in action.
- **What it does:** Simulates a sequence of 50 AI events, transitioning from stable to unstable and back.
- **Key Concepts:**
    - `ICEWLogger`: Telemetry logging.
    - State Transitions: `SOVEREIGN` -> `DEGRADED` -> `INVALIDATED` (or Recovery).
    - Certificate Generation: Produces a JSON audit certificate.
- **Run:**
  ```bash
  python examples/01_basic_sap_audit.py
  ```

### 2. MEBA Calculation (`02_meba_calculation.py`)
Demonstrates the **Marco de Evaluación de Bienestar Algorítmico (MEBA)**.
- **What it does:** Calculates the `MEBA_Cert` score based on a set of simulated user interactions (positive and negative).
- **Key Concepts:**
    - `MEBACalculator`: Computing aggregation.
    - Metrics: RIPN (Ratio of Positive/Negative), FRN (Negative Time Retention).
- **Run:**
  ```bash
  python examples/02_meba_calculation.py
  ```

### 3. Stress Test Demo (`03_stress_test_demo.py`)
A combined demonstration of SAP and MEBA under adversarial conditions.
- **What it does:** Simulates a "Boiling Frog" scenario where system noise (ambiguity) increases linearly.
- **Outcome:** Shows how the SAP protocol detects the drift and eventually triggers the **Fail-Safe** mechanism (`BLOCK_OUTPUT`) to prevent harmful operation.
- **Run:**
  ```bash
  python examples/03_stress_test_demo.py
  ```

## License
© 2024-2026 AHI 3.0 · AHI Governance Labs
