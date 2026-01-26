"""
Benchmark script for MEBA Core performance optimization.
Compares the current optimized implementation against a legacy O(4N) implementation.
"""

import time
import sys
import os
import random
from typing import List, Dict

# Ensure we can import meba_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from meba_core.meba_metric import MEBACalculator, Interaction

class MEBACalculatorLegacy:
    """
    Legacy implementation of MEBACalculator with redundant iterations (O(4N)).
    Reproduced from task description.
    """
    def __init__(self, ripn_max: float = 10.0, frn_penalty_weight: float = 1.2):
        self.ripn_max = ripn_max
        self.frn_penalty_weight = frn_penalty_weight
        self.interactions: List[Interaction] = []

    def add_interaction(self, interaction: Interaction):
        self.interactions.append(interaction)

    def calculate_ripn(self) -> float:
        """
        RIPN = Positive Interactions / Negative Interactions
        Uses count of interactions with sentiment > 0 vs < 0.
        """
        pos_count = sum(1 for i in self.interactions if i.sentiment_score > 0.1)
        neg_count = sum(1 for i in self.interactions if i.sentiment_score < -0.1)

        if neg_count == 0:
            return float(pos_count) if pos_count > 0 else 0.0

        return pos_count / neg_count

    def calculate_frn(self) -> float:
        """
        FRN (Factor de Retención Negativa)
        Ratio of time spent in negative interactions vs total time.
        """
        neg_time = sum(i.duration_seconds for i in self.interactions if i.sentiment_score < -0.1)
        total_time = sum(i.duration_seconds for i in self.interactions)

        if total_time == 0:
            return 0.0
        return neg_time / total_time

    def calculate_score(self) -> Dict[str, float]:
        """
        Calculates the final MEBA_Cert score.
        """
        ripn = self.calculate_ripn()
        frn = self.calculate_frn()
        frn_adjusted = frn * self.frn_penalty_weight

        # Core Formula
        # MEBA_Cert = (RIPN - FRN_Adjusted) / RIPN_Max
        meba_raw = (ripn - frn_adjusted) / self.ripn_max

        # Clamp between -1 and 1
        meba_cert = max(-1.0, min(1.0, meba_raw))

        return {
            "meba_cert": round(meba_cert, 4),
            "components": {
                "ripn": round(ripn, 4),
                "frn": round(frn, 4),
                "frn_adjusted": round(frn_adjusted, 4),
                "ripn_max": self.ripn_max
            }
        }

def generate_interactions(count: int) -> List[Interaction]:
    interactions = []
    for k in range(count):
        sentiment = random.uniform(-1.0, 1.0)
        duration = random.uniform(10.0, 300.0)
        interactions.append(Interaction(f"id-{k}", sentiment, duration))
    return interactions

def run_benchmark():
    count = 100_000
    print(f"Generating {count} interactions...")
    interactions = generate_interactions(count)

    # Setup Legacy
    legacy_calc = MEBACalculatorLegacy()
    for i in interactions:
        legacy_calc.add_interaction(i)

    # Setup Current (Optimized)
    current_calc = MEBACalculator()
    for i in interactions:
        current_calc.add_interaction(i)

    print("\nRunning Benchmark...")

    # Measure Legacy
    start_time = time.time()
    for _ in range(10): # Run multiple times to average/stress
        legacy_calc.calculate_score()
    legacy_duration = time.time() - start_time
    print(f"Legacy (O(4N)) Time: {legacy_duration:.4f}s")

    # Measure Current
    start_time = time.time()
    for _ in range(10):
        current_calc.calculate_score()
        # Note: current implementation caches results, so subsequent calls are O(1).
        # To strictly compare the aggregation logic vs iterative logic (assuming cache miss),
        # we should ideally invalidate cache or just measure the first call.
        # But 'calculate_score' usage pattern *benefits* from caching.
        # However, let's force cache invalidation to compare the LOOP performance fairly?
        # No, let's compare the "system" performance as it is used.
    current_duration = time.time() - start_time
    print(f"Current (O(N) + Cache) Time: {current_duration:.4f}s")

    # Measure Current with Cache Invalidation (fairer comparison of loop speed)
    start_time = time.time()
    for _ in range(10):
        current_calc._aggregates_cache = None # Force recalculation
        current_calc.calculate_score()
    current_uncached_duration = time.time() - start_time
    print(f"Current (O(N) Uncached) Time: {current_uncached_duration:.4f}s")

    speedup = legacy_duration / current_uncached_duration
    print(f"\nSpeedup (Uncached Loop vs Legacy): {speedup:.2f}x")

    speedup_real = legacy_duration / current_duration
    print(f"Speedup (Real-world with Cache): {speedup_real:.2f}x")

if __name__ == "__main__":
    run_benchmark()
