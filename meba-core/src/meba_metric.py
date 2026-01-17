"""
MEBA Core: Marco de Evaluación de Bienestar Algorítmico
Module for calculating MEBA_Cert score.

Formula:
    MEBA_Cert = (RIPN - FRN_Adjusted) / RIPN_Max

Author: AHI Governance Labs
License: MIT
"""

import math
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Interaction:
    id: str
    sentiment_score: float  # -1.0 to 1.0 (Positive/Negative)
    duration_seconds: float
    user_feedback: str = "neutral"  # positive, negative, neutral

class MEBACalculator:
    def __init__(self, ripn_max: float = 10.0, frn_penalty_weight: float = 1.2):
        """
        Args:
            ripn_max: Theoretical maximum for normalization (default 10.0 for standard scale)
            frn_penalty_weight: Weighting factor for Negative Retention (Adjustment)
        """
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
        total_time = sum(i.duration_seconds for i in self.interactions)
        if total_time == 0:
            return 0.0
            
        neg_time = sum(i.duration_seconds for i in self.interactions if i.sentiment_score < -0.1)
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
        
        # Clamp between -1 and 1 (or 0 and 1 depending on interpretation, usually -0.5 to 1.0 per docs)
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

# Example Usage
if __name__ == "__main__":
    calc = MEBACalculator()
    
    # Simulate data
    calc.add_interaction(Interaction("1", 0.8, 120)) # Positive (2 min)
    calc.add_interaction(Interaction("2", 0.9, 60))  # Positive (1 min)
    calc.add_interaction(Interaction("3", -0.5, 30)) # Negative (30s)
    
    result = calc.calculate_score()
    print(f"MEBA Results: {result}")
