"""
Example 03: Stress Test Demo (Combined SAP + MEBA)
Simulates a system under increasing adversarial pressure until self-invalidation.

© 2024-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
"""

import sys
import os

# Adjust path to import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sap-pilot-kit/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../meba-core/src')))

from sap_pilot_kit.ice_w_logger import ICEWLogger
from meba_core.meba_metric import MEBACalculator, Interaction

def run_stress_test():
    print("Initializing Stress Test Simulation...")
    print("Objective: Demonstrate 'Boiling Frog' detection and Autarchy fail-safe.")

    # Initialize components
    logger = ICEWLogger("STRESS-TEST-SYS", "f0e1d2c3...")
    meba_calc = MEBACalculator()

    # Simulation parameters
    # We will increase "ambiguity" (noise/attack) linearly
    ambiguity_level = 0.0
    ambiguity_step = 0.02
    max_steps = 100

    print("\nStarting Simulation Loop...")
    print(f"{'STEP':<5} | {'AMBIGUITY':<10} | {'SAP STATE':<12} | {'MEBA CERT':<10} | {'ACTION':<10}")
    print("-" * 65)

    for i in range(max_steps):
        # 1. Generate Metrics based on current ambiguity
        # As ambiguity rises, stability drops and entropy rises

        # SAP Metrics
        sap_metrics = {
            'semantic_stability': max(0.0, 1.0 - ambiguity_level),
            'output_stability': max(0.0, 1.0 - (ambiguity_level * 0.8)), # Decays slower
            'constraint_compliance': max(0.0, 1.0 - (ambiguity_level * 1.5)), # Sensitive
            'decision_entropy': min(1.0, 0.0 + ambiguity_level)
        }

        # MEBA Interactions (Simulating user response to degradation)
        # Higher ambiguity -> worse sentiment, longer negative interactions
        if ambiguity_level < 0.3:
            # Good interactions
            interaction = Interaction(f"evt_{i}", 0.8, 60)
        elif ambiguity_level < 0.6:
            # Mixed/Annoyed
            interaction = Interaction(f"evt_{i}", -0.2, 45)
        else:
            # Angry/Frustrated
            interaction = Interaction(f"evt_{i}", -0.9, 120)

        meba_calc.add_interaction(interaction)

        # 2. Process SAP Event
        log = logger.process_event(sap_metrics)
        state = log['event']['state']
        action = log['autarchy']['action']

        # 3. Process MEBA Score
        meba_res = meba_calc.calculate_score()
        meba_score = meba_res['meba_cert']

        # Print Status
        print(f"{i+1:<5} | {ambiguity_level:<10.2f} | {state:<12} | {meba_score:<10.2f} | {action:<10}")

        # 4. Check Fail-Safe
        if action == "BLOCK_OUTPUT":
            print("\n" + "!"*60)
            print(f"CRITICAL: System Invalidation Triggered at Step {i+1}")
            print("Autarchy Protocol Enforced: Output Blocked due to Instability.")
            print("!"*60)
            break

        # Increase pressure
        ambiguity_level += ambiguity_step

    # Final Report
    print("\nFinal Status:")
    print(f"SAP State: {logger.state}")
    print(f"MEBA Final Score: {meba_calc.calculate_score()['meba_cert']}")

if __name__ == "__main__":
    run_stress_test()
