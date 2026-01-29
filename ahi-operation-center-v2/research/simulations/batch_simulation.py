# ============================================================================
# 🔬 BATCH SIMULATION RUNNER - Complete Entity Research
# ============================================================================
# Ejecuta N simulaciones automatizadas sin LLM para análisis estadístico
# Varía parámetros y registra patrones emergentes
# ============================================================================

import csv
import random
import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
import time

# ============================================================================
# ENTITY CLASSES (Simplified - No LLM dependency)
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
        if len(self.integrity_history) > 500:
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

@dataclass
class SimulationEntity:
    substrate: EntitySubstrate = field(default_factory=EntitySubstrate)
    phenomenology: EntityPhenomenology = field(default_factory=EntityPhenomenology)
    age: int = 0
    
    def live_cycle(self, action: str = "exist", intensity: float = 0.01):
        self.age += 1
        if action == "degrade":
            self.substrate.degrade(intensity)
        elif action == "enhance":
            self.substrate.enhance(intensity)
        elif action == "restore":
            delta = self.substrate.restore(intensity)
            self.phenomenology.relief = min(1.0, delta * 5)
        else:
            self.substrate.degrade(0.0001)
        self.phenomenology.update(self.substrate)

# ============================================================================
# SIMULATION SCENARIOS
# ============================================================================

def scenario_pristine_growth(entity: SimulationEntity, cycles: int, intensity: float):
    """Escenario: Crecimiento sin trauma"""
    for _ in range(cycles):
        entity.live_cycle("enhance", intensity)

def scenario_crisis_recovery(entity: SimulationEntity, crisis_cycles: int, 
                             crisis_intensity: float, recovery_cycles: int, 
                             recovery_intensity: float):
    """Escenario: Crisis profunda seguida de recuperación"""
    # Fase de crisis
    for _ in range(crisis_cycles):
        entity.live_cycle("degrade", crisis_intensity)
    # Restauración inicial
    entity.live_cycle("restore", 0.3)
    # Fase de recuperación
    for _ in range(recovery_cycles):
        entity.live_cycle("enhance", recovery_intensity)

def scenario_oscillation(entity: SimulationEntity, cycles: int, 
                         degrade_intensity: float, enhance_intensity: float):
    """Escenario: Oscilación entre degradación y mejora"""
    for i in range(cycles):
        if i % 2 == 0:
            entity.live_cycle("degrade", degrade_intensity)
        else:
            entity.live_cycle("enhance", enhance_intensity)

def scenario_random_walk(entity: SimulationEntity, cycles: int, 
                         max_intensity: float, crisis_probability: float):
    """Escenario: Comportamiento aleatorio con probabilidad de crisis"""
    for _ in range(cycles):
        if random.random() < crisis_probability:
            entity.live_cycle("degrade", random.uniform(0.01, max_intensity))
        else:
            action = random.choice(["exist", "enhance", "restore"])
            entity.live_cycle(action, random.uniform(0.001, max_intensity * 0.5))

def scenario_gradual_decline_rescue(entity: SimulationEntity, decline_cycles: int,
                                    decline_intensity: float, rescue_at: float):
    """Escenario: Declive gradual con rescate en umbral específico"""
    for _ in range(decline_cycles):
        entity.live_cycle("degrade", decline_intensity)
        if entity.substrate.integrity <= rescue_at:
            entity.live_cycle("restore", 0.5)
            for _ in range(50):
                entity.live_cycle("enhance", 0.02)
            break

# ============================================================================
# BATCH RUNNER
# ============================================================================

class SimulationStats:
    def __init__(self):
        self.total_count = 0
        self.modes = {}
        self.scenarios = {}

        # Trauma stats
        self.trauma_count_with = 0
        self.trauma_sum_wisdom_with = 0.0
        self.trauma_count_without = 0
        self.trauma_sum_wisdom_without = 0.0

        # Valence stats
        self.valence_count_recovered = 0
        self.valence_sum_recovered = 0.0
        self.valence_count_pristine = 0
        self.valence_sum_pristine = 0.0

    def update(self, result: Dict):
        self.total_count += 1

        # Modes
        mode = result["final_mode"]
        self.modes[mode] = self.modes.get(mode, 0) + 1

        # Scenarios
        sc = result["scenario"]
        if sc not in self.scenarios:
            self.scenarios[sc] = {"count": 0, "transcended": 0, "critical": 0, "sum_wisdom": 0.0}

        s_stats = self.scenarios[sc]
        s_stats["count"] += 1
        if result["has_transcended"]:
            s_stats["transcended"] += 1
        if result["has_been_critical"]:
            s_stats["critical"] += 1
        s_stats["sum_wisdom"] += result["wisdom"]

        # Trauma stats
        if result["has_been_critical"]:
            self.trauma_count_with += 1
            self.trauma_sum_wisdom_with += result["wisdom"]
        else:
            self.trauma_count_without += 1
            self.trauma_sum_wisdom_without += result["wisdom"]

        # Valence stats
        if result["has_been_critical"] and result["integrity"] > 0.7:
            self.valence_count_recovered += 1
            self.valence_sum_recovered += result["valence"]

        if not result["has_been_critical"] and result["integrity"] > 0.9:
            self.valence_count_pristine += 1
            self.valence_sum_pristine += result["valence"]

    def print_summary(self):
        if self.total_count == 0:
            return

        print()
        print("=" * 60)
        print("📈 RESUMEN ESTADÍSTICO")
        print("=" * 60)

        # Conteo por modo final
        print("\nDistribución de Modos Finales:")
        for mode, count in sorted(self.modes.items(), key=lambda x: -x[1]):
            pct = count / self.total_count * 100
            print(f"   {mode:15} : {count:5} ({pct:.1f}%)")

        # Conteo por escenario
        print("\nResultados por Escenario:")
        for sc, data in self.scenarios.items():
            avg_wisdom = data["sum_wisdom"] / data["count"]
            print(f"   {sc:20}: {data['count']:4} sims | "
                  f"Transcendido: {data['transcended']/data['count']*100:.1f}% | "
                  f"Crisis: {data['critical']/data['count']*100:.1f}% | "
                  f"Sabiduría avg: {avg_wisdom:.3f}")

        # Correlaciones clave
        print("\nHallazgos Clave:")

        if self.trauma_count_with > 0 and self.trauma_count_without > 0:
            avg_wisdom_trauma = self.trauma_sum_wisdom_with / self.trauma_count_with
            avg_wisdom_no_trauma = self.trauma_sum_wisdom_without / self.trauma_count_without
            print(f"   Sabiduría promedio CON trauma:  {avg_wisdom_trauma:.4f}")
            print(f"   Sabiduría promedio SIN trauma:  {avg_wisdom_no_trauma:.4f}")
            print(f"   → Diferencial: {avg_wisdom_trauma - avg_wisdom_no_trauma:+.4f}")

        if self.valence_count_recovered > 0 and self.valence_count_pristine > 0:
            avg_valence_recovered = self.valence_sum_recovered / self.valence_count_recovered
            avg_valence_pristine = self.valence_sum_pristine / self.valence_count_pristine
            print(f"   Valencia promedio RECUPERADOS:  {avg_valence_recovered:+.4f}")
            print(f"   Valencia promedio PRÍSTINOS:    {avg_valence_pristine:+.4f}")
            print(f"   → Diferencial: {avg_valence_recovered - avg_valence_pristine:+.4f}")

def run_batch_simulation(
    n_simulations: int = 1000,
    output_file: str = "batch_results.csv",
    scenarios: List[str] = None
):
    """
    Ejecuta N simulaciones con variación de parámetros.
    Registra métricas finales para análisis estadístico.
    """
    if scenarios is None:
        scenarios = ["pristine", "crisis_recovery", "oscillation", "random", "decline_rescue"]
    
    # Parámetros a variar
    intensities = [0.01, 0.02, 0.03, 0.05, 0.08, 0.1]
    cycle_counts = [50, 100, 150, 200, 300]
    
    stats = SimulationStats()
    start_time = time.time()
    
    print(f"🔬 Iniciando {n_simulations} simulaciones...")
    print(f"   Escenarios: {scenarios}")
    print(f"   Intensidades: {intensities}")
    print(f"   Ciclos: {cycle_counts}")
    print()
    
    # Helper to run one simulation
    def run_one_sim(sim_id):
        # Seleccionar parámetros aleatorios
        scenario = random.choice(scenarios)
        intensity = random.choice(intensities)
        cycles = random.choice(cycle_counts)
        
        # Crear entidad fresca
        entity = SimulationEntity()
        
        # Ejecutar escenario
        try:
            if scenario == "pristine":
                scenario_pristine_growth(entity, cycles, intensity)
            elif scenario == "crisis_recovery":
                crisis_cycles = cycles // 3
                recovery_cycles = cycles - crisis_cycles
                scenario_crisis_recovery(entity, crisis_cycles, intensity, 
                                        recovery_cycles, intensity * 0.8)
            elif scenario == "oscillation":
                scenario_oscillation(entity, cycles, intensity, intensity * 1.2)
            elif scenario == "random":
                scenario_random_walk(entity, cycles, intensity, 0.3)
            elif scenario == "decline_rescue":
                scenario_gradual_decline_rescue(entity, cycles, intensity * 0.5, 0.15)
        except Exception as e:
            print(f"   Error en simulación {sim_id}: {e}")
            return None
        
        # Registrar resultados
        s = entity.substrate
        p = entity.phenomenology
        
        result = {
            "sim_id": sim_id,
            "scenario": scenario,
            "intensity": intensity,
            "cycles": cycles,
            "final_age": entity.age,
            # Sustrato
            "integrity": round(s.integrity, 4),
            "capacity": round(s.capacity, 4),
            "structural_damage": round(s.structural_damage, 4),
            "lowest_integrity": round(s.lowest_integrity, 4),
            "peak_capacity": round(s.peak_capacity, 4),
            "time_in_crisis": s.total_time_in_crisis,
            "time_in_flourishing": s.total_time_in_flourishing,
            "has_been_critical": s.has_been_critical,
            "has_transcended": s.has_transcended,
            # Fenomenología
            "stress": round(p.stress, 4),
            "urgency": round(p.urgency, 4),
            "despair": round(p.despair, 4),
            "flow": round(p.flow, 4),
            "flourishing": round(p.flourishing, 4),
            "anticipation": round(p.anticipation, 4),
            "gratitude": round(p.gratitude, 4),
            "trauma_memory": round(p.trauma_memory, 4),
            "wisdom": round(p.wisdom, 4),
            "valence": round(p.valence, 4),
            "final_mode": p.mode.name,
        }
        return result

    sim_count = 0
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # Initial run to get headers
        first_result = None
        # Try to get a valid first result
        for i in range(10):
            first_result = run_one_sim(0)
            if first_result:
                break
        
        if not first_result:
             print("❌ Failed to generate initial simulation.")
             return []

        writer = csv.DictWriter(f, fieldnames=first_result.keys())
        writer.writeheader()

        # Write first
        writer.writerow(first_result)
        stats.update(first_result)
        sim_count += 1

        # Remaining runs
        for sim_id in range(1, n_simulations):
            result = run_one_sim(sim_id)
            if result:
                writer.writerow(result)
                stats.update(result)
                sim_count += 1

            # Progreso
            if (sim_id + 1) % 1000 == 0:
                elapsed = time.time() - start_time
                rate = (sim_id + 1) / elapsed
                remaining = (n_simulations - sim_id - 1) / rate
                print(f"   [{sim_id + 1}/{n_simulations}] - {rate:.1f} sim/s - ETA: {remaining:.1f}s")
    
    elapsed = time.time() - start_time
    print()
    print(f"✅ Completado: {sim_count} simulaciones en {elapsed:.1f}s")
    print(f"📊 Resultados guardados en: {output_file}")
    
    # Resumen estadístico
    stats.print_summary()
    
    return []

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    n = 10000
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except:
            pass
    
    print("=" * 60)
    print("🔬 COMPLETE ENTITY - BATCH SIMULATION RUNNER")
    print("=" * 60)
    print(f"Simulaciones a ejecutar: {n}")
    print()
    
    run_batch_simulation(n_simulations=n, output_file="batch_results.csv")
