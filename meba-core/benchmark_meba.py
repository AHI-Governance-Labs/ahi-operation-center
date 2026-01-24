
import time
import random
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from meba_core.meba_metric import MEBACalculator, Interaction

def generate_interactions(n):
    print(f"Generating {n} interactions...")
    interactions = []
    for i in range(n):
        sentiment = random.uniform(-1.0, 1.0)
        duration = random.uniform(10.0, 300.0)
        interactions.append(Interaction(str(i), sentiment, duration))
    return interactions

def run_benchmark():
    n = 1_000_000
    interactions = generate_interactions(n)

    calc = MEBACalculator()
    # Pre-populate to measure calculation time only, not append time
    calc.interactions = interactions

    print("Starting benchmark for calculate_score...")
    start_time = time.time()
    score = calc.calculate_score()
    end_time = time.time()

    print(f"Calculation took {end_time - start_time:.4f} seconds")
    print(f"Result: {score['meba_cert']}")

if __name__ == "__main__":
    run_benchmark()
