import time
import sys
import os

# Add ahi-operation-center-v2 to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from research.simulations.alpha_autonomous_simulation import EntitySubstrate

def benchmark():
    entity = EntitySubstrate()
    start_time = time.perf_counter()

    for _ in range(100000):
        entity._update()

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Time taken for 100,000 updates: {duration:.4f} seconds")

if __name__ == "__main__":
    benchmark()
