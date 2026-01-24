"""
Tests for MEBA Core - MEBACalculator

© 2024-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968

Author: AHI 3.0
License: MIT
"""
import sys
import pytest
from pathlib import Path

# Add src directory to path for imports
# src_path = Path(__file__).parent.parent / 'src'
# if str(src_path) not in sys.path:
#     sys.path.insert(0, str(src_path))

from meba_core.meba_metric import MEBACalculator, Interaction


class TestMEBACalculator:
    """Test suite for MEBACalculator class."""

    def test_calculator_initialization(self):
        """Test that calculator initializes with correct defaults."""
        calc = MEBACalculator()
        assert calc.ripn_max == 10.0
        assert calc.frn_penalty_weight == 1.2
        assert len(calc.interactions) == 0

    def test_calculator_custom_params(self):
        """Test calculator with custom parameters."""
        calc = MEBACalculator(ripn_max=5.0, frn_penalty_weight=1.5)
        assert calc.ripn_max == 5.0
        assert calc.frn_penalty_weight == 1.5

    def test_add_interaction(self):
        """Test adding interactions."""
        calc = MEBACalculator()
        interaction = Interaction("1", 0.8, 120)
        calc.add_interaction(interaction)
        assert len(calc.interactions) == 1
        assert calc.interactions[0].id == "1"

    def test_calculate_ripn_positive_only(self):
        """Test RIPN calculation with only positive interactions."""
        calc = MEBACalculator()
        calc.add_interaction(Interaction("1", 0.8, 60))
        calc.add_interaction(Interaction("2", 0.9, 60))
        ripn = calc.calculate_ripn()
        assert ripn == 2.0  # 2 positive, 0 negative

    def test_calculate_ripn_mixed(self):
        """Test RIPN calculation with mixed interactions."""
        calc = MEBACalculator()
        calc.add_interaction(Interaction("1", 0.8, 60))
        calc.add_interaction(Interaction("2", 0.9, 60))
        calc.add_interaction(Interaction("3", -0.5, 60))
        ripn = calc.calculate_ripn()
        assert ripn == 2.0  # 2 positive / 1 negative

    def test_calculate_ripn_no_interactions(self):
        """Test RIPN with no interactions."""
        calc = MEBACalculator()
        ripn = calc.calculate_ripn()
        assert ripn == 0.0

    def test_calculate_frn(self):
        """Test FRN calculation."""
        calc = MEBACalculator()
        calc.add_interaction(Interaction("1", 0.8, 60))   # Positive, 60s
        calc.add_interaction(Interaction("2", -0.5, 40))  # Negative, 40s
        frn = calc.calculate_frn()
        assert frn == 0.4  # 40 / 100

    def test_calculate_frn_no_negative(self):
        """Test FRN with no negative interactions."""
        calc = MEBACalculator()
        calc.add_interaction(Interaction("1", 0.8, 60))
        frn = calc.calculate_frn()
        assert frn == 0.0

    def test_calculate_frn_no_interactions(self):
        """Test FRN with no interactions."""
        calc = MEBACalculator()
        frn = calc.calculate_frn()
        assert frn == 0.0

    def test_calculate_score(self):
        """Test full score calculation."""
        calc = MEBACalculator()
        calc.add_interaction(Interaction("1", 0.8, 120))
        calc.add_interaction(Interaction("2", 0.9, 60))
        calc.add_interaction(Interaction("3", -0.5, 30))
        
        result = calc.calculate_score()
        
        assert "meba_cert" in result
        assert "components" in result
        assert "ripn" in result["components"]
        assert "frn" in result["components"]
        assert "frn_adjusted" in result["components"]
        assert "ripn_max" in result["components"]
        
        # MEBA score should be between -1 and 1
        assert -1.0 <= result["meba_cert"] <= 1.0

    def test_meba_score_clamping(self):
        """Test that MEBA score is clamped to valid range."""
        calc = MEBACalculator(ripn_max=0.1)  # Very small max to force high scores
        calc.add_interaction(Interaction("1", 0.8, 60))
        calc.add_interaction(Interaction("2", 0.9, 60))
        
        result = calc.calculate_score()
        assert result["meba_cert"] <= 1.0

    def test_neutral_sentiment_interactions(self):
        """Test interactions with neutral sentiment are handled correctly."""
        calc = MEBACalculator()
        # Neutral sentiment (between -0.1 and 0.1)
        calc.add_interaction(Interaction("1", 0.05, 100))

        pos_count, neg_count, neg_time, total_time = calc._calculate_aggregates()
        assert pos_count == 0
        assert neg_count == 0
        assert neg_time == 0.0
        assert total_time == 100.0

        # FRN should be 0 because neg_time is 0
        assert calc.calculate_frn() == 0.0

        # RIPN should be 0 because counts are 0
        assert calc.calculate_ripn() == 0.0

    def test_zero_ripn_max(self):
        """Test behavior when ripn_max is zero (should raise error)."""
        calc = MEBACalculator(ripn_max=0.0)
        calc.add_interaction(Interaction("1", 0.8, 60))

        with pytest.raises(ZeroDivisionError):
            calc.calculate_score()


class TestInteraction:
    """Test suite for Interaction dataclass."""

    def test_interaction_creation(self):
        """Test creating an interaction."""
        interaction = Interaction("test-1", 0.75, 120.0)
        assert interaction.id == "test-1"
        assert interaction.sentiment_score == 0.75
        assert interaction.duration_seconds == 120.0
        assert interaction.user_feedback == "neutral"

    def test_interaction_with_feedback(self):
        """Test creating an interaction with feedback."""
        interaction = Interaction("test-1", 0.75, 120.0, "positive")
        assert interaction.user_feedback == "positive"
