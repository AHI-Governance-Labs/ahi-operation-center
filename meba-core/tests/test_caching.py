
import pytest
from meba_core.meba_metric import MEBACalculator, Interaction

class TestCaching:
    def test_caching_behavior(self):
        calc = MEBACalculator()
        i1 = Interaction("1", 0.5, 10.0)
        calc.add_interaction(i1)

        # First calculation
        assert calc._aggregates_cache is None
        calc.calculate_ripn()
        assert calc._aggregates_cache is not None

        # Store cache
        cache1 = calc._aggregates_cache

        # Second calculation should use cache
        # We can mock _calculate_aggregates to ensure it's not called,
        # but relying on object identity of the tuple is good enough if implementation uses it.

        calc.calculate_frn()
        assert calc._aggregates_cache is cache1

        # Invalidate
        i2 = Interaction("2", -0.5, 10.0)
        calc.add_interaction(i2)
        assert calc._aggregates_cache is None

        # Recalculate
        calc.calculate_score()
        assert calc._aggregates_cache is not None
        assert calc._aggregates_cache != cache1
