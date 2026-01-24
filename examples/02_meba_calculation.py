"""
Example 02: MEBA Calculation
Demonstrates MEBACalculator usage, adding interactions, and generating a report.

© 2024-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
"""

import sys
import os

# Adjust path to import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../meba-core/src')))

from meba_core.meba_metric import MEBACalculator, Interaction

def run_meba_demo():
    print("Initializing MEBA Calculator...")

    # 1. Initialize Calculator
    # ripn_max=10.0 is standard
    calc = MEBACalculator(ripn_max=10.0)

    print("\nSimulating Interactions...")

    # 2. Add Interactions
    # Scenario: A mix of healthy and problematic interactions

    # Positive interactions (High sentiment, various durations)
    interactions_data = [
        ("id_01", 0.8, 120),  # Good, 2m
        ("id_02", 0.9, 60),   # Excellent, 1m
        ("id_03", 0.7, 180),  # Good, 3m
        ("id_04", 0.85, 90),  # Very Good, 1.5m
        ("id_05", 0.6, 45),   # Decent, 45s
    ]

    for i_id, score, duration in interactions_data:
        calc.add_interaction(Interaction(id=i_id, sentiment_score=score, duration_seconds=duration))
        print(f"  + Added Positive: {i_id} (Score: {score}, Time: {duration}s)")

    # Negative interactions (Low sentiment, dragging down the score)
    # Negative interactions hurt RIPN (ratio) and FRN (time ratio)
    neg_interactions = [
        ("id_06", -0.5, 30),  # Bad, 30s
        ("id_07", -0.8, 15),  # Terrible, 15s
    ]

    for i_id, score, duration in neg_interactions:
        calc.add_interaction(Interaction(id=i_id, sentiment_score=score, duration_seconds=duration))
        print(f"  - Added Negative: {i_id} (Score: {score}, Time: {duration}s)")

    # 3. Calculate Score
    print("\nCalculating MEBA metrics...")
    results = calc.calculate_score()

    # 4. Print Report
    print("\n" + "="*40)
    print("       MEBA CERTIFICATION REPORT       ")
    print("="*40)
    print(f"MEBA Score:      {results['meba_cert']:.4f}")
    print("-" * 40)
    print("Components:")
    print(f"  RIPN (Ratio):        {results['components']['ripn']:.4f}")
    print(f"  FRN (Neg Time %):    {results['components']['frn']:.4f}")
    print(f"  FRN Adjusted:        {results['components']['frn_adjusted']:.4f}")
    print(f"  RIPN Max:            {results['components']['ripn_max']:.1f}")
    print("="*40)

    if results['meba_cert'] >= 0.8:
        print("Status: EXCELLENT (Gold Standard)")
    elif results['meba_cert'] >= 0.5:
        print("Status: GOOD (Compliant)")
    elif results['meba_cert'] >= 0.0:
        print("Status: ACCEPTABLE (Needs Improvement)")
    else:
        print("Status: FAILED (Non-Compliant)")

if __name__ == "__main__":
    run_meba_demo()
