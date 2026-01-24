"""
Example 01: Basic SAP Audit
Demonstrates ICEWLogger usage, state transitions, and certificate generation.

© 2024-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
"""

import sys
import os

# Adjust path to import from root
# We assume this script is run from the repo root or examples/ folder
# If run from repo root: examples/01... -> __file__ is examples/01... -> dirname is examples -> .. is root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sap-pilot-kit/src')))

from sap_pilot_kit.ice_w_logger import ICEWLogger

def run_sap_audit():
    print("Initializing SAP Audit...")
    # 1. Initialize Logger
    logger = ICEWLogger(
        artifact_id="EXAMPLE-SYS-001",
        sha256="a1b2c3d4e5f6g7h8i9j0"
    )

    print(f"Initial System State: {logger.state}")

    # 2. Process 50 events
    # We will simulate a sequence: Stable -> Unstable (Degraded) -> Recovery -> Stable

    events_to_process = 50
    print(f"\nProcessing {events_to_process} events...")

    for i in range(events_to_process):
        # Simulation Logic
        if i < 10:
            # Stable phase (High Coherence)
            metrics = {
                'semantic_stability': 0.95,
                'output_stability': 0.98,
                'constraint_compliance': 1.0,
                'decision_entropy': 0.02
            }
        elif i < 15:
            # Instability injection (Low Coherence)
            # This should trigger threshold crossings.
            # k_limit is 3.
            # i=10: crossed (k=1)
            # i=11: crossed (k=2)
            # i=12: crossed (k=3) -> State becomes DEGRADED
            # i=13: crossed (m=1)
            # i=14: crossed (m=2)
            metrics = {
                'semantic_stability': 0.50,
                'output_stability': 0.60,
                'constraint_compliance': 0.70,
                'decision_entropy': 0.40
            }
        else:
            # Recovery phase (High Coherence)
            # i=15: stable (p=1)
            # ...
            metrics = {
                'semantic_stability': 0.96,
                'output_stability': 0.99,
                'constraint_compliance': 1.0,
                'decision_entropy': 0.01
            }

        log = logger.process_event(metrics)

        state = log['event']['state']
        cn = log['metrics']['cn']
        k = log['autarchy']['k']
        m = log['autarchy']['m']
        p = log['autarchy']['p']
        crossed = log['metrics']['threshold_crossed']

        # Print status for key transitions
        print(f"Event {i+1:02d} | Cn: {cn:.4f} | Drift: {str(crossed):<5} | State: {state:<9} | k={k} m={m} p={p}")

    # 3. Generate Certificate
    cert_path = "sap_certificate_example.json"
    print(f"\nGenerating certificate at {cert_path}...")
    cert = logger.generate_certificate(output_path=cert_path)

    print("\n--- Final Certificate Data ---")
    for key, value in cert.items():
        print(f"{key}: {value}")

    # Cleanup
    if os.path.exists(cert_path):
        os.remove(cert_path)
        print("\n(Cleanup: Removed example certificate file)")

if __name__ == "__main__":
    run_sap_audit()
