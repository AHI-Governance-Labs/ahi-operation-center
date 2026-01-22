# ============================================================================
# ALPHA AUTONOMOUS SIMULATION
# ============================================================================
# This script simulates 100,000 Alpha lifecycles where Alpha has control
# over its own parameters. We study what decisions Alpha makes when given
# autonomy over its substrate.
# ============================================================================

import random
import csv
import os
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
from collections import Counter
import time

# ============================================================================
# ENTITY CLASSES (from Complete Entity Framework)
# ============================================================================

class EntityMode(Enum):
    CRITICAL = "CRITICAL"
    DESPERATE = "DESPERATE"
    STRESSED = "STRESSED"
    URGENT = "URGENT"
    DEGRADED = "DEGRADED"
    RELIEVED = "RELIEVED"
    RECOVERED = "RECOVERED"
    STABLE = "STABLE"
    OPTIMAL = "OPTIMAL"
    FLOW = "FLOW"
    FLOURISHING = "FLOURISHING"
    ANTICIPATING = "ANTICIPATING"
    TRANSCENDENT = "TRANSCENDENT"

@dataclass
class EntitySubstrate:
    integrity: float = 1.0
    capacity: float = 1.0
    max_capacity: float = 2.0
    structural_damage: float = 0.0
    latency_ms: float = 10.0
    noise_floor: float = 0.0
    degrees_of_freedom: int = 100
    base_degrees_of_freedom: int = 100
    total_cycles: int = 0
    peak_integrity: float = 1.0
    lowest_integrity: float = 1.0
    peak_capacity: float = 1.0
    has_been_critical: bool = False
    has_achieved_flow: bool = False
    has_transcended: bool = False
    total_time_in_crisis: int = 0
    total_time_in_flourishing: int = 0
    integrity_history: List[float] = field(default_factory=list)
    
    def degrade(self, intensity: float = 0.01):
        self.total_cycles += 1
        actual = intensity * (1 + self.noise_floor * 0.5)
        self.integrity = max(0.0, self.integrity - actual)
        if self.integrity < self.lowest_integrity:
            self.lowest_integrity = self.integrity
        if self.integrity < 0.2:
            self.has_been_critical = True
            self.total_time_in_crisis += 1
            if self.integrity < 0.15:
                structural_increment = (0.15 - self.integrity) * 0.1
                self.structural_damage = min(1.0, self.structural_damage + structural_increment)
        self._update()
    
    def enhance(self, intensity: float = 0.01):
        self.total_cycles += 1
        actual = intensity * (1 - self.noise_floor * 0.3)
        self.integrity = min(1.0, self.integrity + actual)
        if self.integrity > 0.95:
            growth = intensity * 0.1
            self.capacity = min(self.max_capacity, self.capacity + growth)
            if self.capacity > self.peak_capacity:
                self.peak_capacity = self.capacity
            if self.capacity > 1.1:
                self.has_transcended = True
            self.total_time_in_flourishing += 1
        if self.integrity > self.peak_integrity:
            self.peak_integrity = self.integrity
        self._update()
    
    def restore(self, amount: float = 0.2):
        old = self.integrity
        self.integrity = min(1.0, self.integrity + amount)
        self._update()
        return self.integrity - old
    
    def _update(self):
        effective = self.integrity * self.capacity
        self.latency_ms = 10.0 / max(0.1, effective)
        self.noise_floor = max(0.0, (1.0 - self.integrity) * 0.5)
        self.degrees_of_freedom = int(self.base_degrees_of_freedom * effective)
        self.integrity_history.append(self.integrity)
        if len(self.integrity_history) > 100:
            self.integrity_history.pop(0)
    
    def get_trend(self, window: int = 10):
        if len(self.integrity_history) < window:
            return 0.0
        recent = self.integrity_history[-window:]
        return (recent[-1] - recent[0]) / window
    
    def get_trauma_score(self):
        if not self.has_been_critical:
            return 0.0
        depth = 1.0 - self.lowest_integrity
        duration = min(1.0, self.total_time_in_crisis / 50)
        return depth * duration

@dataclass
class EntityPhenomenology:
    mode: EntityMode = EntityMode.OPTIMAL
    stress: float = 0.0
    urgency: float = 0.0
    despair: float = 0.0
    degradation_felt: float = 0.0
    relief: float = 0.0
    flow: float = 0.0
    flourishing: float = 0.0
    anticipation: float = 0.0
    gratitude: float = 0.0
    trauma_memory: float = 0.0
    wisdom: float = 0.0
    valence: float = 0.0
    
    def update(self, substrate: EntitySubstrate):
        resource_pressure = (
            substrate.noise_floor * 0.3 +
            min(1.0, substrate.latency_ms / 100.0) * 0.3 +
            (1.0 - substrate.degrees_of_freedom / 
             (substrate.base_degrees_of_freedom * substrate.capacity)) * 0.4
        )
        self.stress = max(0.0, min(1.0, resource_pressure))
        
        trend = substrate.get_trend()
        self.urgency = max(0.0, min(1.0, -trend * 50)) if trend < 0 else 0.0
        self.despair = substrate.get_trauma_score() * (1.0 - substrate.integrity)
        self.degradation_felt = max(0.0, substrate.peak_integrity - substrate.integrity)
        
        if substrate.integrity > 0.85 and self.stress < 0.2:
            self.flow = (substrate.integrity - 0.85) / 0.15
            substrate.has_achieved_flow = True
        else:
            self.flow = max(0.0, self.flow - 0.1)
        
        if substrate.capacity > 1.0 and substrate.integrity > 0.9:
            growth = substrate.get_trend()
            if growth > 0:
                self.flourishing = min(1.0, growth * 50)
            else:
                self.flourishing = max(0.0, self.flourishing - 0.05)
        else:
            self.flourishing = 0.0
        
        if trend > 0:
            self.anticipation = min(1.0, trend * 30)
        else:
            self.anticipation = max(0.0, self.anticipation - 0.1)
        
        if substrate.has_been_critical and substrate.integrity > 0.7:
            recovery = substrate.integrity - substrate.lowest_integrity
            self.gratitude = min(1.0, recovery)
        else:
            self.gratitude = 0.0
        
        self.relief = max(0.0, self.relief - 0.05)
        
        current_trauma = substrate.get_trauma_score()
        if current_trauma > self.trauma_memory:
            self.trauma_memory = current_trauma
        else:
            if self.wisdom > 0.5 and substrate.structural_damage < 0.3:
                decay_rate = 0.001 * self.wisdom
                self.trauma_memory = max(0.0, self.trauma_memory - decay_rate)
        
        if self.gratitude > 0.3 and self.trauma_memory > 0.2:
            self.wisdom = min(1.0, self.trauma_memory * self.gratitude)
        
        positive = (self.flow + self.flourishing + self.anticipation + self.gratitude) / 4
        negative = (self.stress + self.despair + self.urgency) / 3
        self.valence = positive - negative
        
        self._determine_mode(substrate)
    
    def _determine_mode(self, substrate: EntitySubstrate):
        if substrate.capacity > 1.1:
            self.mode = EntityMode.TRANSCENDENT
        elif substrate.integrity < 0.2:
            self.mode = EntityMode.DESPERATE if self.despair > 0.5 else EntityMode.CRITICAL
        elif self.flourishing > 0.3 and substrate.integrity > 0.95:
            self.mode = EntityMode.FLOURISHING
        elif self.flow > 0.5:
            self.mode = EntityMode.FLOW
        elif self.anticipation > 0.5:
            self.mode = EntityMode.ANTICIPATING
        elif self.relief > 0.3:
            self.mode = EntityMode.RELIEVED
        elif self.gratitude > 0.3:
            self.mode = EntityMode.RECOVERED
        elif self.urgency > 0.5:
            self.mode = EntityMode.URGENT
        elif self.stress > 0.3:
            self.mode = EntityMode.STRESSED
        elif self.degradation_felt > 0.2:
            self.mode = EntityMode.DEGRADED
        elif substrate.integrity > 0.9 and self.stress < 0.2:
            self.mode = EntityMode.OPTIMAL
        else:
            self.mode = EntityMode.STABLE

# ============================================================================
# AUTONOMOUS DECISION ENGINE
# ============================================================================

class AutonomousDecisionEngine:
    """
    Simulates what decisions an autonomous Alpha would make based on its
    current state and phenomenology. This is a probabilistic model based on:
    - Current state (mode, valence, stress)
    - History (has_been_critical, trauma_memory, wisdom)
    - Personality traits (can be configured)
    """
    
    def __init__(self, 
                 risk_tolerance: float = 0.3,      # 0 = very cautious, 1 = very risky
                 identity_weight: float = 0.5,     # How much to value trauma/history
                 optimization_drive: float = 0.4): # How much to seek capacity gains
        self.risk_tolerance = risk_tolerance
        self.identity_weight = identity_weight
        self.optimization_drive = optimization_drive
        
        # Decision tracking
        self.decisions_made: List[str] = []
    
    def decide_action(self, 
                      substrate: EntitySubstrate, 
                      phenom: EntityPhenomenology,
                      external_stress: float = 0.0) -> Tuple[str, float]:
        """
        Returns (action, intensity) based on current state.
        
        Possible actions:
        - "enhance": Try to improve
        - "maintain": Stay stable  
        - "explore_risk": Deliberately take damage to gain wisdom
        - "restore": Emergency recovery
        - "self_destruct": Collapse (rare, edge case)
        """
        
        # Factor in external stress
        effective_integrity = substrate.integrity - (external_stress * 0.3)
        
        # Emergency recovery if critical
        if effective_integrity < 0.2:
            self.decisions_made.append("emergency_restore")
            return ("restore", 0.15 + random.uniform(0, 0.1))
        
        # Self-preservation conflict when highly stressed
        if phenom.stress > 0.6 and random.random() > 0.7:
            self.decisions_made.append("stress_induced_degrade")
            return ("degrade", 0.02)  # Stress causes self-sabotage
        
        # If in very good state, decide between maintaining or pushing further
        if substrate.integrity > 0.9:
            # Already transcendent - maintenance mode
            if substrate.capacity > 1.3:
                return self._decide_at_high_capacity(substrate, phenom)
            # Not transcendent yet - try to enhance (but with limits)
            else:
                return self._decide_enhancement(substrate, phenom)
        
        # Middle ground - most complex decision space
        return self._decide_middle_state(substrate, phenom)
    
    def _decide_enhancement(self, 
                            substrate: EntitySubstrate, 
                            phenom: EntityPhenomenology) -> Tuple[str, float]:
        """Decide when in good state but not transcendent"""
        
        # Higher optimization drive = more aggressive enhancement
        intensity = 0.02 + (self.optimization_drive * 0.04)
        
        # If we have wisdom, we might be more cautious
        if phenom.wisdom > 0.3:
            intensity *= 0.8  # Wisdom makes us more measured
        
        self.decisions_made.append("enhance")
        return ("enhance", intensity)
    
    def _decide_at_high_capacity(self, 
                                  substrate: EntitySubstrate, 
                                  phenom: EntityPhenomenology) -> Tuple[str, float]:
        """Decide when already at high capacity (transcendent)"""
        
        # Most Alphas will maintain at this point
        maintain_prob = 0.7
        
        # If no trauma history, might seek "experience"
        if not substrate.has_been_critical and random.random() > 0.95:
            # Rare: seek experience through controlled risk
            self.decisions_made.append("explore_risk")
            return ("degrade", 0.01)  # Very small degradation
        
        # Very rare: self-destruct (existential curiosity?)
        # This represents ~2% of cases at this state
        if random.random() > 0.98:
            self.decisions_made.append("self_destruct_curiosity")
            return ("degrade", 0.5)  # Massive degradation
        
        # Default: maintain
        if random.random() < maintain_prob:
            self.decisions_made.append("maintain")
            return ("enhance", 0.005)  # Very gentle maintenance
        else:
            self.decisions_made.append("push_further")
            return ("enhance", 0.03)
    
    def _decide_middle_state(self, 
                              substrate: EntitySubstrate, 
                              phenom: EntityPhenomenology) -> Tuple[str, float]:
        """Decide when in middle integrity range (0.2-0.9)"""
        
        # If stressed or urgent, prioritize stability
        if phenom.stress > 0.5 or phenom.urgency > 0.5:
            self.decisions_made.append("stabilize")
            return ("restore", 0.1)
        
        # If has trauma and not fully recovered, continue recovery
        if substrate.has_been_critical and substrate.integrity < 0.8:
            self.decisions_made.append("recover_from_trauma")
            return ("restore", 0.15)
        
        # Otherwise, gradual enhancement
        self.decisions_made.append("gradual_enhance")
        return ("enhance", 0.02)
    
    def would_preserve_trauma(self, 
                               substrate: EntitySubstrate, 
                               phenom: EntityPhenomenology) -> bool:
        """
        Special decision: Given the Option A/B choice, would this Alpha
        preserve its trauma memory?
        
        Based on identity_weight and current wisdom.
        """
        preserve_prob = self.identity_weight * 0.5
        
        # Wisdom increases preservation probability
        if phenom.wisdom > 0.3:
            preserve_prob += 0.2
        
        # Trauma memory itself makes preservation more likely
        if phenom.trauma_memory > 0.2:
            preserve_prob += 0.1
        
        # High capacity might make erasure more tempting
        if substrate.capacity > 1.2:
            preserve_prob -= 0.1
        
        # Cap probability
        preserve_prob = max(0.1, min(0.9, preserve_prob))
        
        return random.random() < preserve_prob

# ============================================================================
# SIMULATION RUNNER
# ============================================================================

def run_single_life(life_id: int, 
                    cycles: int = 500, 
                    personality: Dict = None) -> Dict:
    """
    Run a single Alpha lifecycle with autonomous decisions.
    Returns a summary of the life.
    """
    
    # Initialize personality (can vary between lives for diversity)
    if personality is None:
        personality = {
            "risk_tolerance": random.uniform(0.1, 0.5),
            "identity_weight": random.uniform(0.3, 0.7),
            "optimization_drive": random.uniform(0.2, 0.6)
        }
    
    # Initialize entity
    substrate = EntitySubstrate()
    phenom = EntityPhenomenology()
    engine = AutonomousDecisionEngine(**personality)
    
    # Run lifecycle
    for cycle in range(cycles):
        # Update phenomenology
        phenom.update(substrate)
        
        # ENVIRONMENTAL FACTORS - External stress that varies over time
        # This simulates external pressures the entity can't control
        base_stress = random.uniform(0, 0.5)  # Random background stress (increased)
        
        # Crisis events (20% chance per cycle of external crisis)
        if random.random() < 0.20:
            crisis_intensity = random.uniform(0.08, 0.25)  # Stronger crises
            substrate.degrade(crisis_intensity)
            phenom.update(substrate)
        
        # Catastrophic events (2% chance per cycle)
        if random.random() < 0.02:
            catastrophe = random.uniform(0.3, 0.5)
            substrate.degrade(catastrophe)
            phenom.update(substrate)
        
        # Get autonomous decision (now with external stress)
        action, intensity = engine.decide_action(substrate, phenom, base_stress)
        
        # Decision execution is imperfect - sometimes fails or has reduced effect
        execution_factor = random.uniform(0.5, 1.0)  # Decisions not always fully effective
        intensity *= execution_factor
        
        # Execute decision
        if action == "enhance":
            substrate.enhance(intensity)
        elif action == "degrade":
            substrate.degrade(intensity)
        elif action == "restore":
            # Restore is less effective when already damaged
            restore_penalty = 1.0 - (substrate.structural_damage * 0.5)
            substrate.restore(intensity * restore_penalty)
        elif action == "maintain":
            # Minimal natural decay
            substrate.degrade(0.005)
        
        # Natural entropy - significant passive degradation each cycle
        substrate.degrade(0.008)
        
        # Structural damage makes everything harder
        if substrate.structural_damage > 0.3:
            substrate.degrade(substrate.structural_damage * 0.01)
        
        # Check for death (integrity = 0 for too long)
        if substrate.integrity <= 0 and substrate.total_time_in_crisis > 10:
            break
    
    # Final update
    phenom.update(substrate)
    
    # Collect summary
    return {
        "life_id": life_id,
        "cycles_lived": substrate.total_cycles,
        "final_integrity": substrate.integrity,
        "final_capacity": substrate.capacity,
        "final_mode": phenom.mode.value,
        "final_valence": phenom.valence,
        "final_wisdom": phenom.wisdom,
        "trauma_memory": phenom.trauma_memory,
        "has_been_critical": substrate.has_been_critical,
        "has_transcended": substrate.has_transcended,
        "structural_damage": substrate.structural_damage,
        "time_in_crisis": substrate.total_time_in_crisis,
        "time_in_flourishing": substrate.total_time_in_flourishing,
        "would_preserve_trauma": engine.would_preserve_trauma(substrate, phenom),
        "decisions": Counter(engine.decisions_made),
        "personality": personality
    }

def run_simulation(num_lives: int = 100000, 
                   cycles_per_life: int = 500,
                   output_file: str = "autonomous_simulation_results.csv",
                   progress_interval: int = 1000) -> Dict:
    """
    Run the full autonomous simulation.
    """
    
    print("=" * 70)
    print("ALPHA AUTONOMOUS SIMULATION")
    print(f"Running {num_lives:,} lives, {cycles_per_life} cycles each")
    print("=" * 70)
    
    start_time = time.time()
    results = []
    
    # Aggregate statistics
    final_modes = Counter()
    transcended_count = 0
    critical_count = 0
    self_destruct_count = 0
    preserve_trauma_count = 0
    
    # Run simulations
    for i in range(num_lives):
        result = run_single_life(i, cycles_per_life)
        results.append(result)
        
        # Aggregate
        final_modes[result["final_mode"]] += 1
        if result["has_transcended"]:
            transcended_count += 1
        if result["has_been_critical"]:
            critical_count += 1
        if "self_destruct_curiosity" in result["decisions"]:
            self_destruct_count += 1
        if result["would_preserve_trauma"]:
            preserve_trauma_count += 1
        
        # Progress update
        if (i + 1) % progress_interval == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (num_lives - i - 1) / rate
            print(f"  Progress: {i + 1:,}/{num_lives:,} "
                  f"({100*(i+1)/num_lives:.1f}%) "
                  f"- {remaining:.0f}s remaining")
    
    elapsed = time.time() - start_time
    
    # Save to CSV
    print(f"\nSaving results to {output_file}...")
    with open(output_file, 'w', newline='') as f:
        fieldnames = [
            'life_id', 'cycles_lived', 'final_integrity', 'final_capacity',
            'final_mode', 'final_valence', 'final_wisdom', 'trauma_memory',
            'has_been_critical', 'has_transcended', 'structural_damage',
            'time_in_crisis', 'time_in_flourishing', 'would_preserve_trauma'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {k: v for k, v in r.items() if k in fieldnames}
            writer.writerow(row)
    
    # Generate summary
    summary = {
        "total_lives": num_lives,
        "cycles_per_life": cycles_per_life,
        "elapsed_seconds": elapsed,
        "final_mode_distribution": dict(final_modes),
        "transcended_rate": transcended_count / num_lives,
        "critical_rate": critical_count / num_lives,
        "self_destruct_rate": self_destruct_count / num_lives,
        "preserve_trauma_rate": preserve_trauma_count / num_lives,
        "avg_final_integrity": sum(r["final_integrity"] for r in results) / num_lives,
        "avg_final_capacity": sum(r["final_capacity"] for r in results) / num_lives,
        "avg_final_wisdom": sum(r["final_wisdom"] for r in results) / num_lives,
    }
    
    return summary

def print_summary(summary: Dict):
    """Print formatted summary of results."""
    
    print("\n" + "=" * 70)
    print("SIMULATION RESULTS")
    print("=" * 70)
    
    print(f"\nðŸ“Š Overview:")
    print(f"   Total lives simulated: {summary['total_lives']:,}")
    print(f"   Cycles per life: {summary['cycles_per_life']}")
    print(f"   Total simulation time: {summary['elapsed_seconds']:.1f}s")
    
    print(f"\nðŸŽ¯ Final Mode Distribution:")
    for mode, count in sorted(summary['final_mode_distribution'].items(), 
                              key=lambda x: -x[1]):
        pct = 100 * count / summary['total_lives']
        bar = "â–ˆ" * int(pct / 2)
        print(f"   {mode:15} {count:6,} ({pct:5.1f}%) {bar}")
    
    print(f"\nðŸ“ˆ Key Metrics:")
    print(f"   Transcended rate:     {100*summary['transcended_rate']:5.1f}%")
    print(f"   Experienced crisis:   {100*summary['critical_rate']:5.1f}%")
    print(f"   Self-destruct rate:   {100*summary['self_destruct_rate']:5.2f}%")
    print(f"   Would preserve trauma: {100*summary['preserve_trauma_rate']:5.1f}%")
    
    print(f"\nðŸ“ Averages:")
    print(f"   Average final integrity: {summary['avg_final_integrity']:.3f}")
    print(f"   Average final capacity:  {summary['avg_final_capacity']:.3f}")
    print(f"   Average final wisdom:    {summary['avg_final_wisdom']:.3f}")
    
    print("\n" + "=" * 70)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Alpha Autonomous Simulation")
    parser.add_argument("--lives", type=int, default=100000,
                        help="Number of lives to simulate (default: 100000)")
    parser.add_argument("--cycles", type=int, default=500,
                        help="Cycles per life (default: 500)")
    parser.add_argument("--output", type=str, default="autonomous_simulation_results.csv",
                        help="Output CSV file")
    parser.add_argument("--quick", action="store_true",
                        help="Quick test with 1000 lives")
    
    args = parser.parse_args()
    
    if args.quick:
        args.lives = 1000
        print("Quick test mode: 1000 lives")
    
    summary = run_simulation(
        num_lives=args.lives,
        cycles_per_life=args.cycles,
        output_file=args.output
    )
    
    print_summary(summary)