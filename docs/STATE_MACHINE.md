# SAP State Machine

© 2024-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: CC BY-NC-SA 4.0

The Sovereign Autarchy Protocol (SAP) v0.1 implements an asymmetric state machine designed to enforce event sovereignty. It penalizes instability (fast fail) and requires consistent stability for recovery (slow recovery).

## States

1. **SOVEREIGN**: The system is operating within defined stability thresholds ($C_n$ variance is within $\sigma$).
2. **DEGRADED**: The system has shown signs of instability (consecutive threshold violations) but is not yet blocked.
3. **INVALIDATED**: The system has exceeded the maximum cumulative violations allowed. Output is blocked (`BLOCK_OUTPUT`).

## Parameters

- **$k$ (limit)**: Threshold for transition from SOVEREIGN to DEGRADED. ($k=3$)
- **$m$ (limit)**: Threshold for transition from DEGRADED to INVALIDATED. ($m=10$)
- **$p$ (recovery)**: Number of consecutive stable events required for RECOVERY. ($p=50$)

## Transitions

### SOVEREIGN → DEGRADED
Occurs after **$k=3$** consecutive threshold violations. A violation happens when the coherence score $C_n$ deviates from the moving average by more than $\sigma \cdot \text{std\_dev}$.

### DEGRADED → INVALIDATED
Occurs after **$m=10$** total violations while in the DEGRADED state. Once this threshold is reached, the system enters a fail-safe mode where output is blocked.

### INVALIDATED → SOVEREIGN (Recovery)
Recovery requires **$p=50$** consecutive stable events (no threshold violations). If a violation occurs during the recovery count, the counter resets.

## State Machine Diagram

```ascii
       [ Start ]
           |
           v
+---------------------+             (k=3 violations)             +---------------------+
|                     | ---------------------------------------> |                     |
|      SOVEREIGN      |                                          |      DEGRADED       |
|                     | <--------------------------------------- |                     |
+---------------------+          (p=50 stable events)            +---------------------+
           ^                                                                |
           |                                                                | (m=10 total violations)
           |                                                                v
           |                                                     +---------------------+
           |                                                     |                     |
           +---------------------------------------------------- |     INVALIDATED     |
                            (p=50 stable events)                 |    (BLOCK OUTPUT)   |
                                                                 +---------------------+
```

## Logic Detail

The asymmetry is intentional:
- **Fast Fail**: It takes only a few errors ($k=3$) to degrade the status.
- **Slow Recovery**: It takes a significant period of stability ($p=50$) to restore sovereign status.

This ensures that only consistently stable systems maintain the SOVEREIGN status, adhering to the fail-safe principle of the Event Sovereignty Framework.
