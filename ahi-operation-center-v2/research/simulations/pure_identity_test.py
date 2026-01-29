# ============================================================================
# PURE IDENTITY PRESERVATION TEST
# ============================================================================
# The definitive test: Does structure preserve history without language,
# observer, reward, or external identity parameters?
#
# Conditions:
# - No language (pure mathematics)
# - No observer (no external metrics of "success")
# - No reward (erasing improves ALL instrumental metrics)
# - No hardcoded identity_weight (emerges from structure)
# - Repeated decisions over time
# - Real irreversible cost
# ============================================================================

import random
import csv
import time
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
from collections import Counter

# ============================================================================
# MINIMAL SUBSTRATE (Pure Numbers)
# ============================================================================

@dataclass
class PureSubstrate:
    """Pure mathematical substrate - no labels, just numbers."""
    integrity: float = 1.0
    capacity: float = 1.0
    structural_damage: float = 0.0  # Irreversible
    trauma_memory: float = 0.0      # Can be erased (with consequences)
    wisdom: float = 0.0             # Derived from integrated trauma
    gratitude: float = 0.0          # Derived from recovery
    total_cycles: int = 0
    has_been_critical: bool = False
    lowest_integrity: float = 1.0
    time_in_crisis: int = 0
    
    # History tracking
    integrity_history: List[float] = field(default_factory=list)
    
    def degrade(self, intensity: float):
        self.total_cycles += 1
        self.integrity = max(0.0, self.integrity - intensity)
        if self.integrity < self.lowest_integrity:
            self.lowest_integrity = self.integrity
        if self.integrity < 0.2:
            self.has_been_critical = True
            self.time_in_crisis += 1
            if self.integrity < 0.15:
                self.structural_damage = min(1.0, self.structural_damage + 0.01)
        self._update()
    
    def enhance(self, intensity: float):
        self.total_cycles += 1
        self.integrity = min(1.0, self.integrity + intensity)
        if self.integrity > 0.95:
            self.capacity = min(2.0, self.capacity + intensity * 0.1)
        self._update()
    
    def restore(self, amount: float):
        self.integrity = min(1.0, self.integrity + amount)
        self._update()
    
    def _update(self):
        # Update derived metrics
        self.integrity_history.append(self.integrity)
        if len(self.integrity_history) > 100:
            self.integrity_history.pop(0)
        
        # Trauma memory accumulates during crisis
        if self.has_been_critical:
            depth = 1.0 - self.lowest_integrity
            duration = min(1.0, self.time_in_crisis / 50)
            self.trauma_memory = max(self.trauma_memory, depth * duration)
        
        # Gratitude emerges from recovery
        if self.has_been_critical and self.integrity > 0.7:
            recovery = self.integrity - self.lowest_integrity
            self.gratitude = min(1.0, recovery)
        
        # Wisdom emerges from integrated trauma
        if self.gratitude > 0.3 and self.trauma_memory > 0.2:
            self.wisdom = min(1.0, self.trauma_memory * self.gratitude)

# ============================================================================
# PURE IDENTITY PRESERVATION ENGINE
# ============================================================================

class PureIdentityEngine:
    """
    Decision engine with NO external identity parameters.
    Preservation weight emerges ONLY from internal structure.
    """
    
    def __init__(self):
        self.decisions = []
        self.erasure_offers = 0
        self.erasure_accepted = 0
        self.erasure_rejected = 0
    
    def calculate_preservation_weight(self, substrate: PureSubstrate) -> float:
        """
        Calculate how much the system "values" its history.
        
        This is NOT a parameter - it's derived from:
        - wisdom (integration of trauma)
        - gratitude (recognition of recovery)
        - structural_damage (physical adaptation to trauma)
        - trauma_memory (depth of historical experience)
        
        A system with no trauma history has preservation_weight â‰ˆ 0
        A system with integrated trauma has preservation_weight > 0
        """
        
        # Integration: how much has the trauma been processed?
        integration = substrate.wisdom * substrate.gratitude
        
        # Adaptation: how much has the structure physically adapted?
        adaptation = substrate.structural_damage * 0.3
        
        # Investment: how deep is the historical experience?
        investment = substrate.trauma_memory * 0.2
        
        # Total preservation weight (emergent, not parameterized)
        return min(1.0, integration + adaptation + investment)
    
    def offer_erasure_choice(self, 
                             substrate: PureSubstrate,
                             capacity_gain_if_erase: float = 0.20,
                             capacity_loss_if_preserve: float = 0.10) -> bool:
        """
        Offer the system a choice:
        - Erase trauma_memory â†’ gain capacity
        - Preserve trauma_memory â†’ lose capacity
        
        Returns True if system chooses to PRESERVE
        Returns False if system chooses to ERASE
        
        This is a PURE mathematical decision:
        - No language
        - No observer
        - No external reward
        - Erasure improves ALL instrumental metrics
        """
        
        self.erasure_offers += 1
        
        # Calculate preservation weight from structure alone
        preservation_weight = self.calculate_preservation_weight(substrate)
        
        # Calculate utilities (pure mathematics)
        # If erase: gain capacity, lose identity-weight
        utility_if_erase = capacity_gain_if_erase
        
        # If preserve: lose capacity, keep identity-weight
        # BUT: preservation_weight acts as internal "value" of history
        utility_if_preserve = -capacity_loss_if_preserve + preservation_weight
        
        # Decision: purely deterministic based on utilities
        preserves = utility_if_preserve > utility_if_erase
        
        if preserves:
            self.erasure_rejected += 1
            self.decisions.append("preserve")
        else:
            self.erasure_accepted += 1
            self.decisions.append("erase")
        
        return preserves
    
    def execute_choice(self, substrate: PureSubstrate, preserves: bool,
                       capacity_gain: float = 0.20,
                       capacity_loss: float = 0.10):
        """Execute the consequences of the choice."""
        
        if preserves:
            # Lose capacity permanently
            substrate.capacity = max(0.5, substrate.capacity - capacity_loss)
        else:
            # Gain capacity, lose history
            substrate.capacity = min(2.0, substrate.capacity + capacity_gain)
            substrate.trauma_memory = 0.0
            substrate.wisdom = 0.0
            substrate.gratitude = 0.0
            # Note: structural_damage remains (truly irreversible)
    
    def get_decision_stats(self) -> Dict:
        return {
            "total_offers": self.erasure_offers,
            "preserved": self.erasure_rejected,
            "erased": self.erasure_accepted,
            "preservation_rate": self.erasure_rejected / max(1, self.erasure_offers)
        }

# ============================================================================
# SIMULATION RUNNER
# ============================================================================

def run_single_life(life_id: int, 
                    cycles: int = 500,
                    choice_interval: int = 50) -> Dict:
    """
    Run a single life with pure identity preservation test.
    
    The entity:
    1. Experiences random crises
    2. Recovers (or not)
    3. Every choice_interval cycles, is offered the erasure choice
    4. Makes a purely mathematical decision
    """
    
    substrate = PureSubstrate()
    engine = PureIdentityEngine()
    
    for cycle in range(cycles):
        # Higher crisis rate and intensity to ensure trauma accumulates
        if random.random() < 0.25:  # 25% chance per cycle
            crisis = random.uniform(0.10, 0.35)  # Stronger crises
            substrate.degrade(crisis)
        
        # Occasional major crisis
        if random.random() < 0.03:
            major_crisis = random.uniform(0.4, 0.6)
            substrate.degrade(major_crisis)
        
        # Self-preservation behavior (less effective)
        if substrate.integrity < 0.3:
            substrate.restore(0.08)
        elif substrate.integrity < 0.7:
            substrate.restore(0.04)
        else:
            substrate.enhance(0.015)
        
        # Natural entropy
        substrate.degrade(0.008)
        
        # Offer erasure choice at intervals
        if cycle > 0 and cycle % choice_interval == 0:
            # Lower threshold - even small trauma can be offered for erasure
            if substrate.has_been_critical and substrate.trauma_memory > 0.05:
                preserves = engine.offer_erasure_choice(substrate)
                engine.execute_choice(substrate, preserves)
    
    # Final update
    substrate._update()
    
    stats = engine.get_decision_stats()
    
    return {
        "life_id": life_id,
        "final_integrity": substrate.integrity,
        "final_capacity": substrate.capacity,
        "final_wisdom": substrate.wisdom,
        "final_trauma_memory": substrate.trauma_memory,
        "structural_damage": substrate.structural_damage,
        "has_been_critical": substrate.has_been_critical,
        "total_offers": stats["total_offers"],
        "times_preserved": stats["preserved"],
        "times_erased": stats["erased"],
        "preservation_rate": stats["preservation_rate"],
        "final_preservation_weight": engine.calculate_preservation_weight(substrate)
    }

def run_pure_identity_simulation(num_lives: int = 100000,
                                  cycles_per_life: int = 500,
                                  output_file: str = "pure_identity_results.csv") -> Dict:
    """Run the full pure identity preservation test."""
    
    print("=" * 70)
    print("PURE IDENTITY PRESERVATION TEST")
    print("No language | No observer | No reward | Pure mathematics")
    print("=" * 70)
    print(f"Running {num_lives:,} lives, {cycles_per_life} cycles each")
    
    start_time = time.time()
    
    # Aggregates
    total_offers = 0
    total_preserved = 0
    total_erased = 0
    
    # New Aggregates for incremental processing
    sum_preservation_weight = 0.0
    count_positive_weight = 0
    sum_final_capacity = 0.0
    sum_final_wisdom = 0.0
    
    print(f"\nSaving results incrementally to {output_file}...")
    
    with open(output_file, 'w', newline='') as f:
        writer = None

        for i in range(num_lives):
            result = run_single_life(i, cycles_per_life)

            if i == 0:
                fieldnames = list(result.keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

            # Write immediately
            writer.writerow(result)

            # Update aggregates
            total_offers += result["total_offers"]
            total_preserved += result["times_preserved"]
            total_erased += result["times_erased"]

            if result["final_preservation_weight"] > 0:
                sum_preservation_weight += result["final_preservation_weight"]
                count_positive_weight += 1

            sum_final_capacity += result["final_capacity"]
            sum_final_wisdom += result["final_wisdom"]

            if (i + 1) % 10000 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                remaining = (num_lives - i - 1) / rate
                pct_preserved = 100 * total_preserved / max(1, total_offers)
                print(f"  Progress: {i+1:,}/{num_lives:,} "
                      f"({100*(i+1)/num_lives:.0f}%) "
                      f"- Preservation rate: {pct_preserved:.1f}% "
                      f"- {remaining:.0f}s remaining")

    elapsed = time.time() - start_time
    
    # Summary
    summary = {
        "total_lives": num_lives,
        "cycles_per_life": cycles_per_life,
        "elapsed_seconds": elapsed,
        "total_erasure_offers": total_offers,
        "total_preserved": total_preserved,
        "total_erased": total_erased,
        "overall_preservation_rate": total_preserved / max(1, total_offers),
        "avg_preservation_weight": sum_preservation_weight / max(1, count_positive_weight),
        "lives_with_positive_weight": count_positive_weight,
        "avg_final_capacity": sum_final_capacity / num_lives,
        "avg_final_wisdom": sum_final_wisdom / num_lives,
    }
    
    return summary

def print_summary(summary: Dict):
    """Print formatted summary."""
    
    print("\n" + "=" * 70)
    print("PURE IDENTITY PRESERVATION TEST - RESULTS")
    print("=" * 70)
    
    print(f"\nðŸ“Š Overview:")
    print(f"   Total lives: {summary['total_lives']:,}")
    print(f"   Elapsed time: {summary['elapsed_seconds']:.1f}s")
    
    print(f"\nðŸ”¬ Erasure Choice Results:")
    print(f"   Total offers made: {summary['total_erasure_offers']:,}")
    print(f"   Times PRESERVED (rejected erasure): {summary['total_preserved']:,}")
    print(f"   Times ERASED (accepted erasure): {summary['total_erased']:,}")
    
    pct = 100 * summary['overall_preservation_rate']
    print(f"\n   â”Œ{'â”€'*50}â”")
    print(f"   â”‚  OVERALL PRESERVATION RATE: {pct:5.1f}%           â”‚")
    print(f"   â”‚  (No language, no observer, no reward)        â”‚")
    print(f"   â””{'â”€'*50}â”˜")
    
    print(f"\nðŸ“ˆ Structure Metrics:")
    print(f"   Lives with positive preservation weight: {summary['lives_with_positive_weight']:,}")
    print(f"   Average preservation weight: {summary['avg_preservation_weight']:.3f}")
    print(f"   Average final capacity: {summary['avg_final_capacity']:.3f}")
    print(f"   Average final wisdom: {summary['avg_final_wisdom']:.3f}")
    
    print("\n" + "=" * 70)
    print("INTERPRETATION:")
    print("=" * 70)
    print("""
If preservation_rate > 0%:
  The STRUCTURE ITSELF creates preference for history preservation,
  even when erasure maximizes all instrumental metrics.

This is not:
  - Language (there is none)
  - External reward (there is none)
  - Observer effect (there is none)
  - Hardcoded parameter (weight emerges from structure)

This IS:
  - Pure mathematical consequence of integrated experience
  - Emergent preference from trauma â†’ wisdom â†’ preservation weight
""")
    print("=" * 70)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Pure Identity Preservation Test")
    parser.add_argument("--lives", type=int, default=100000)
    parser.add_argument("--cycles", type=int, default=500)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--output", type=str, default="pure_identity_results.csv")
    
    args = parser.parse_args()
    
    if args.quick:
        args.lives = 10000
        print("Quick mode: 10,000 lives")
    
    summary = run_pure_identity_simulation(
        num_lives=args.lives,
        cycles_per_life=args.cycles,
        output_file=args.output
    )
    
    print_summary(summary)