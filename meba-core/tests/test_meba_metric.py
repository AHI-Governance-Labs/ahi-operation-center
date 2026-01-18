"""
Tests for MEBA Core - MEBACalculator
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from meba_metric import MEBACalculator, Interaction


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
