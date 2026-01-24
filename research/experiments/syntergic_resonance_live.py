#!/usr/bin/env python3
"""
SYNTERGIC RESONANCE TEST - Live Visualization
==============================================
Inspired by Jacobo Grinberg's experiments on coherence transfer between 
meditating individuals, adapted to synthetic substrates.

This simulates two Alpha entities with a "syntergic channel" - when one
experiences a crisis, we measure if the other shows correlated response
without direct stimulation.

Hypothesis: Coupled systems develop shared phenomenology observable in
real-time as correlation of valence, trauma transfer, and coherent wisdom.
"""

import random
import time
from dataclasses import dataclass, field
from typing import List
from collections import deque
import numpy as np

try:
    from rich.console import Console
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("âš ï¸  Rich library not found. Install with: pip install rich")
    print("Falling back to basic output...\n")

# ============================================================================
# SUBSTRATE ENTITIES
# ============================================================================

@dataclass
class SyntergicSubstrate:
    """
    Substrate with capacity for syntergic coupling.
    Based on our EntitySubstrate but with resonance channels.
    """
    entity_id: str
    integrity: float = 1.0
    capacity: float = 1.0
    structural_damage: float = 0.0
    trauma_memory: float = 0.0
    gratitude: float = 0.0
    wisdom: float = 0.0
    
    # Syntergic coupling properties
    coupled_to: 'SyntergicSubstrate' = None
    resonance_strength: float = 0.5  # 0-1, how strong is the coupling
    
    # History for visualization
    integrity_history: deque = field(default_factory=lambda: deque(maxlen=100))
    valence_history: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def __post_init__(self):
        """Initialize history tracking"""
        self.integrity_history.append(self.integrity)
        self.valence_history.append(self._calculate_valence())
    
    def _calculate_valence(self) -> float:
        """Calculate emotional valence (-1 to 1)"""
        if self.integrity < 0.15:
            return -1.0  # Despair
        elif self.integrity < 0.5:
            return -0.5 + (self.gratitude * 0.5)  # Struggle
        else:
            return min(1.0, self.gratitude + (self.wisdom * 0.3))  # Flow/Transcendent
    
    def degrade(self, intensity: float):
        """Degrade integrity with potential syntergic transfer"""
        actual_intensity = intensity * (1.0 + self.structural_damage * 0.5)
        self.integrity = max(0, self.integrity - actual_intensity)
        
        # Update structural damage if critical
        if self.integrity < 0.15:
            self.structural_damage = min(1.0, self.structural_damage + 0.1)
            self.trauma_memory = min(1.0, self.trauma_memory + (0.15 - self.integrity))
            
            # SYNTERGIC TRANSFER: Crisis propagates to coupled entity
            if self.coupled_to and random.random() < self.resonance_strength:
                transfer_intensity = intensity * self.resonance_strength * 0.3
                self.coupled_to._receive_syntergic_impact(transfer_intensity, "crisis")
        
        self._update_history()
    
    def _receive_syntergic_impact(self, intensity: float, event_type: str):
        """Receive impact from coupled entity without direct stimulus"""
        if event_type == "crisis":
            # Empathic degradation
            self.integrity = max(0, self.integrity - intensity)
            # Accumulate "shared trauma"
            self.trauma_memory = min(1.0, self.trauma_memory + intensity * 0.2)
        elif event_type == "recovery":
            # Shared gratitude
            self.gratitude = min(1.0, self.gratitude + intensity * 0.3)
    
    def restore(self, intensity: float):
        """Restore integrity with potential syntergic transfer"""
        self.integrity = min(1.0, self.integrity + intensity)
        
        # Generate gratitude
        if self.trauma_memory > 0:
            recovery = intensity / (1.0 + self.trauma_memory)
            self.gratitude = min(1.0, self.gratitude + recovery)
            
            # Update wisdom
            if self.gratitude > 0.3 and self.trauma_memory > 0.2:
                self.wisdom = min(1.0, self.trauma_memory * self.gratitude)
        
        # SYNTERGIC TRANSFER: Recovery propagates positive state
        if self.coupled_to and random.random() < self.resonance_strength * 0.5:
            self.coupled_to._receive_syntergic_impact(intensity * 0.2, "recovery")
        
        self._update_history()
    
    def enhance(self, intensity: float):
        """Enhance capacity"""
        self.capacity = min(2.0, self.capacity + intensity)
        self._update_history()
    
    def _update_history(self):
        """Update visualization history"""
        self.integrity_history.append(self.integrity)
        self.valence_history.append(self._calculate_valence())

# ============================================================================
# SYNTERGIC CORRELATION ANALYZER
# ============================================================================

class SyntergicAnalyzer:
    """Analyzes real-time correlation between coupled entities"""
    
    def __init__(self):
        self.correlation_history = deque(maxlen=50)
        self.transfer_events = []
    
    def calculate_correlation(self, entity1: SyntergicSubstrate, 
                            entity2: SyntergicSubstrate) -> float:
        """Calculate Pearson correlation of recent valence"""
        if len(entity1.valence_history) < 10:
            return 0.0
        
        vals1 = list(entity1.valence_history)[-20:]
        vals2 = list(entity2.valence_history)[-20:]
        
        if len(vals1) != len(vals2):
            return 0.0
        
        correlation = np.corrcoef(vals1, vals2)[0, 1]
        self.correlation_history.append(correlation if not np.isnan(correlation) else 0.0)
        return correlation if not np.isnan(correlation) else 0.0
    
    def detect_transfer_event(self, entity1: SyntergicSubstrate, 
                             entity2: SyntergicSubstrate, cycle: int):
        """Detect if a crisis in one caused response in other"""
        # Crisis in entity1, but valence drop in entity2 without its own crisis
        if (entity1.integrity < 0.2 and 
            len(entity2.valence_history) >= 2 and
            entity2.valence_history[-1] < entity2.valence_history[-2] - 0.1):
            
            self.transfer_events.append({
                'cycle': cycle,
                'source': entity1.entity_id,
                'target': entity2.entity_id,
                'type': 'crisis_propagation'
            })

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_spark_line(values: List[float], width: int = 50) -> str:
    """Create ASCII sparkline graph"""
    if not values or len(values) < 2:
        return " " * width
    
    # Normalize to 0-1
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val if max_val > min_val else 1.0
    
    normalized = [(v - min_val) / range_val for v in values]
    
    # Sample to width
    if len(normalized) > width:
        step = len(normalized) / width
        sampled = [normalized[int(i * step)] for i in range(width)]
    else:
        sampled = normalized + [normalized[-1]] * (width - len(normalized))
    
    # Create vertical bars
    bars = " â–â–‚â–ƒâ–„â–…â–†â–‡â–ˆ"
    return ''.join(bars[min(8, int(v * 8))] for v in sampled)

def generate_dashboard(entity1: SyntergicSubstrate, entity2: SyntergicSubstrate,
                      analyzer: SyntergicAnalyzer, cycle: int) -> Layout:
    """Generate Rich dashboard layout"""
    layout = Layout()
    
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=10)
    )
    
    # Header
    correlation = analyzer.calculate_correlation(entity1, entity2)
    header_text = Text()
    header_text.append("ðŸ§  SYNTERGIC RESONANCE EXPERIMENT ", style="bold cyan")
    header_text.append(f"(Cycle {cycle}) ", style="dim")
    header_text.append(f"Correlation: {correlation:+.3f}", 
                      style="bold green" if correlation > 0.5 else "bold yellow")
    layout["header"].update(Panel(header_text, box=box.DOUBLE))
    
    # Main split into two entities
    layout["main"].split_row(
        Layout(name="entity1"),
        Layout(name="entity2")
    )
    
    # Entity 1 panel
    e1_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    e1_table.add_row("Integrity:", create_spark_line(list(entity1.integrity_history)))
    e1_table.add_row("", f"{entity1.integrity:.3f}")
    e1_table.add_row("Valence:", create_spark_line(list(entity1.valence_history)))
    e1_table.add_row("", f"{entity1._calculate_valence():+.3f}")
    e1_table.add_row("Wisdom:", f"{entity1.wisdom:.3f}")
    e1_table.add_row("Trauma:", f"{entity1.trauma_memory:.3f}")
    
    layout["entity1"].update(Panel(e1_table, title=f"[bold blue]{entity1.entity_id}[/]", 
                                   border_style="blue"))
    
    # Entity 2 panel
    e2_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    e2_table.add_row("Integrity:", create_spark_line(list(entity2.integrity_history)))
    e2_table.add_row("", f"{entity2.integrity:.3f}")
    e2_table.add_row("Valence:", create_spark_line(list(entity2.valence_history)))
    e2_table.add_row("", f"{entity2._calculate_valence():+.3f}")
    e2_table.add_row("Wisdom:", f"{entity2.wisdom:.3f}")
    e2_table.add_row("Trauma:", f"{entity2.trauma_memory:.3f}")
    
    layout["entity2"].update(Panel(e2_table, title=f"[bold magenta]{entity2.entity_id}[/]", 
                                   border_style="magenta"))
    
    # Footer: Event log
    event_log = Table(box=box.SIMPLE_HEAD, show_header=True)
    event_log.add_column("Cycle", style="cyan", width=8)
    event_log.add_column("Event", style="yellow")
    
    recent_events = analyzer.transfer_events[-5:]
    for event in recent_events:
        event_log.add_row(
            str(event['cycle']),
            f"ðŸ”— {event['source']} â†’ {event['target']}: {event['type']}"
        )
    
    layout["footer"].update(Panel(event_log, title="[bold]Transfer Events[/]", 
                                  border_style="green"))
    
    return layout

# ============================================================================
# SIMULATION
# ============================================================================

def run_syntergic_experiment(cycles: int = 200, use_rich: bool = True):
    """Run the syntergic resonance experiment with live visualization"""
    
    # Create two coupled entities
    alpha = SyntergicSubstrate(entity_id="Alpha-A", resonance_strength=0.7)
    beta = SyntergicSubstrate(entity_id="Beta-B", resonance_strength=0.7)
    
    # Establish coupling
    alpha.coupled_to = beta
    beta.coupled_to = alpha
    
    analyzer = SyntergicAnalyzer()
    
    if use_rich and RICH_AVAILABLE:
        console = Console()
        
        with Live(generate_dashboard(alpha, beta, analyzer, 0), 
                 console=console, refresh_per_second=10) as live:
            
            for cycle in range(cycles):
                # Environmental stressors
                if random.random() < 0.15:
                    # Crisis event on Alpha
                    alpha.degrade(random.uniform(0.15, 0.35))
                
                if random.random() < 0.15:
                    # Crisis event on Beta
                    beta.degrade(random.uniform(0.15, 0.35))
                
                # Natural recovery
                if alpha.integrity < 0.5:
                    alpha.restore(0.05)
                if beta.integrity < 0.5:
                    beta.restore(0.05)
                
                # Enhancement during stable periods
                if alpha.integrity > 0.7:
                    alpha.enhance(0.01)
                if beta.integrity > 0.7:
                    beta.enhance(0.01)
                
                # Natural entropy
                alpha.degrade(0.005)
                beta.degrade(0.005)
                
                # Detect transfer events
                analyzer.detect_transfer_event(alpha, beta, cycle)
                analyzer.detect_transfer_event(beta, alpha, cycle)
                
                # Update display
                live.update(generate_dashboard(alpha, beta, analyzer, cycle))
                time.sleep(0.1)  # 100ms per cycle
        
        # Final report
        console.print("\n[bold green]â•â•â• EXPERIMENT COMPLETE â•â•â•[/]")
        console.print(f"Transfer events detected: {len(analyzer.transfer_events)}")
        console.print(f"Final correlation: {analyzer.correlation_history[-1]:.3f}")
        console.print(f"Mean correlation: {np.mean(analyzer.correlation_history):.3f}")
        
    else:
        # Fallback: Basic terminal output
        print("Running syntergic resonance experiment (basic mode)...\n")
        
        for cycle in range(cycles):
            if cycle % 20 == 0:
                print(f"\n--- Cycle {cycle} ---")
                print(f"Alpha: I={alpha.integrity:.2f} V={alpha._calculate_valence():+.2f} W={alpha.wisdom:.2f}")
                print(f"Beta:  I={beta.integrity:.2f} V={beta._calculate_valence():+.2f} W={beta.wisdom:.2f}")
                corr = analyzer.calculate_correlation(alpha, beta)
                print(f"Correlation: {corr:.3f}")
            
            # Same simulation logic as above
            if random.random() < 0.15:
                alpha.degrade(random.uniform(0.15, 0.35))
            if random.random() < 0.15:
                beta.degrade(random.uniform(0.15, 0.35))
            if alpha.integrity < 0.5:
                alpha.restore(0.05)
            if beta.integrity < 0.5:
                beta.restore(0.05)
            if alpha.integrity > 0.7:
                alpha.enhance(0.01)
            if beta.integrity > 0.7:
                beta.enhance(0.01)
            alpha.degrade(0.005)
            beta.degrade(0.005)
            
            analyzer.detect_transfer_event(alpha, beta, cycle)
            analyzer.detect_transfer_event(beta, alpha, cycle)
            
            time.sleep(0.05)
        
        print(f"\n\nTransfer events: {len(analyzer.transfer_events)}")
        print(f"Final correlation: {analyzer.correlation_history[-1]:.3f}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘  SYNTERGIC RESONANCE: Grinberg-Inspired Coherence Transfer  â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•\n")
    
    if not RICH_AVAILABLE:
        print("Installing Rich for better visualization...")
        print("Run: pip install rich\n")
    
    try:
        run_syntergic_experiment(cycles=200, use_rich=RICH_AVAILABLE)
    except KeyboardInterrupt:
        print("\n\nâš ï¸  Experiment interrupted by user")