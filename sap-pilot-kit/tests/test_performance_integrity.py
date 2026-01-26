import math
import numpy as np
from collections import deque
import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from sap_pilot_kit.ice_w_logger import ICEWLogger

class TestPerformanceIntegrity(unittest.TestCase):
    def test_math_equivalence(self):
        """Verify that pure python math matches numpy math for mean and std."""
        data = [0.1, 0.5, 0.9, 0.3, 0.7, 0.95, 0.05, 0.2, 0.8, 0.4]

        # Numpy Baseline
        np_mean = np.mean(data)
        np_std = np.std(data) # defaults to ddof=0

        # Manual Calculation (as implemented in ICEWLogger)
        w_len = len(data)
        manual_mean = sum(data) / w_len
        variance = sum((x - manual_mean) ** 2 for x in data) / w_len
        manual_std = math.sqrt(variance)

        self.assertAlmostEqual(np_mean, manual_mean, places=9, msg="Mean mismatch")
        self.assertAlmostEqual(np_std, manual_std, places=9, msg="Std mismatch")

    def test_icew_logger_math_integration(self):
        """Verify ICEWLogger uses the logic correctly via process_event."""
        logger = ICEWLogger("TEST", "HASH")

        # Fill window with known data
        data = [0.5] * 100
        # Perturb a bit to have non-zero std
        for i in range(10):
            data[i] = 0.1 * i

        # We need to inject this data into the logger's window
        logger.window = deque(data, maxlen=100)

        # Let's send an event with a known CN
        # metrics that sum to 2.0 -> cn = 0.5
        metrics = {
            'semantic_stability': 0.5,
            'output_stability': 0.5,
            'constraint_compliance': 0.5,
            'decision_entropy': 0.5 # 1 - 0.5 = 0.5
        }
        # cn = (0.5+0.5+0.5+0.5)/4 = 0.5

        log = logger.process_event(metrics)

        # Calculate expected mean
        expected_mean = sum(data) / len(data)
        expected_delta = abs(0.5 - expected_mean)

        self.assertAlmostEqual(log['metrics']['delta'], expected_delta, places=4)

if __name__ == "__main__":
    unittest.main()
