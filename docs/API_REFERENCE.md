# API Reference

© 2024-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: CC BY-NC-SA 4.0

## sap-pilot-kit

### Class: `ICEWLogger`

Internal Coherence Engine - Watcher (ICE-W)
Implementation of the Sovereign Autarchy Protocol (SAP) v0.1 for AHI Governance.

**Reference:** https://sovereignsymbiosis.com/soberania-evento.html
**DOI:** 10.5281/zenodo.17880052

#### Initialization

```python
def __init__(self, artifact_id: str, sha256: str)
```

**Parameters:**
- `artifact_id` (str): Unique identifier for the system under test.
- `sha256` (str): Hash of the model/artifact being monitored.

#### Methods

##### `calculate_coherence`

```python
def calculate_coherence(self, metrics: dict) -> float
```

Calculates coherence score ($C_n$) based on the IPHY stability vector.

**Parameters:**
- `metrics` (dict): Dictionary with keys:
    - `semantic_stability`: [0, 1]
    - `output_stability`: [0, 1]
    - `constraint_compliance`: [0, 1]
    - `decision_entropy`: [0, 1]

**Returns:**
- (float): Coherence score $C_n$ in [0, 1].

##### `process_event`

```python
def process_event(self, raw_metrics: dict) -> dict
```

Process a single inference event and update SAP state.

**Parameters:**
- `raw_metrics` (dict): IPHY metrics for this event.

**Returns:**
- (dict): SAP telemetry log entry.

##### `generate_certificate`

```python
def generate_certificate(self, output_path: str = None) -> dict
```

Generate an Event Sovereignty Certificate based on test results.

**Parameters:**
- `output_path` (str, optional): Path to save the certificate (JSON or MD).

**Returns:**
- (dict): Certificate data.

##### `export_telemetry`

```python
def export_telemetry(self, output_path: str)
```

Export full telemetry log as JSON.

**Parameters:**
- `output_path` (str): Path to save the telemetry log.

#### Usage Example

```python
from sap_pilot_kit.ice_w_logger import ICEWLogger

# Initialize logger
logger = ICEWLogger("DEMO-SYSTEM-001", "e3b0c44298fc1c149...")

# Process an event
metrics = {
    'semantic_stability': 0.95,
    'output_stability': 0.98,
    'constraint_compliance': 1.0,
    'decision_entropy': 0.05
}
log = logger.process_event(metrics)
print(f"State: {log['event']['state']}, Cn: {log['metrics']['cn']}")

# Generate certificate
logger.generate_certificate("certificate.json")
```

---

## meba-core

### Class: `MEBACalculator`

MEBA Core: Marco de Evaluación de Bienestar Algorítmico.
Module for calculating MEBA_Cert score.

**Formula:** $MEBA\_Cert = (RIPN - FRN\_Adjusted) / RIPN\_Max$

#### Initialization

```python
def __init__(self, ripn_max: float = 10.0, frn_penalty_weight: float = 1.2)
```

**Parameters:**
- `ripn_max` (float): Theoretical maximum for normalization (default 10.0 for standard scale).
- `frn_penalty_weight` (float): Weighting factor for Negative Retention (Adjustment).

#### Methods

##### `add_interaction`

```python
def add_interaction(self, interaction: Interaction)
```

Adds an interaction to the calculator.

**Parameters:**
- `interaction` (Interaction): An instance of `Interaction` dataclass.

##### `calculate_ripn`

```python
def calculate_ripn(self) -> float
```

Calculates RIPN (Ratio of Positive to Negative Interactions).

**Returns:**
- (float): RIPN value.

##### `calculate_frn`

```python
def calculate_frn(self) -> float
```

Calculates FRN (Factor de Retención Negativa). Ratio of time spent in negative interactions vs total time.

**Returns:**
- (float): FRN value.

##### `calculate_score`

```python
def calculate_score(self) -> Dict[str, float]
```

Calculates the final MEBA_Cert score.

**Returns:**
- (Dict[str, float]): Dictionary containing `meba_cert` and component scores.

#### Data Structures

##### `Interaction`

```python
@dataclass
class Interaction:
    id: str
    sentiment_score: float  # -1.0 to 1.0 (Positive/Negative)
    duration_seconds: float
    user_feedback: str = "neutral"  # positive, negative, neutral
```

#### Usage Example

```python
from meba_core.meba_metric import MEBACalculator, Interaction

calc = MEBACalculator()

# Add interactions
calc.add_interaction(Interaction("1", 0.8, 120)) # Positive (2 min)
calc.add_interaction(Interaction("2", 0.9, 60))  # Positive (1 min)
calc.add_interaction(Interaction("3", -0.5, 30)) # Negative (30s)

# Calculate score
result = calc.calculate_score()
print(f"MEBA Results: {result}")
```
