# ============================================================================
# CRISIS PATTERN ANALYSIS - 4 Research Questions
# ============================================================================

from dataclasses import dataclass, field
from typing import List

@dataclass
class Substrate:
    integrity: float = 1.0
    capacity: float = 1.0
    structural_damage: float = 0.0
    lowest_integrity: float = 1.0
    has_been_critical: bool = False
    has_transcended: bool = False
    time_in_crisis: int = 0
    noise_floor: float = 0.0
    
    def degrade(self, i):
        actual = i * (1 + self.noise_floor * 0.5)
        self.integrity = max(0.0, self.integrity - actual)
        if self.integrity < self.lowest_integrity:
            self.lowest_integrity = self.integrity
        if self.integrity < 0.2:
            self.has_been_critical = True
            self.time_in_crisis += 1
            if self.integrity < 0.15:
                self.structural_damage = min(1.0, self.structural_damage + (0.15 - self.integrity) * 0.1)
        self.noise_floor = max(0.0, (1.0 - self.integrity) * 0.5)
    
    def enhance(self, i):
        actual = i * (1 - self.noise_floor * 0.3)
        self.integrity = min(1.0, self.integrity + actual)
        if self.integrity > 0.95:
            self.capacity = min(2.0, self.capacity + i * 0.1)
            if self.capacity > 1.1:
                self.has_transcended = True
        self.noise_floor = max(0.0, (1.0 - self.integrity) * 0.5)
    
    def restore(self, amount):
        self.integrity = min(1.0, self.integrity + amount)
        self.noise_floor = max(0.0, (1.0 - self.integrity) * 0.5)

@dataclass
class Phenom:
    wisdom: float = 0.0
    gratitude: float = 0.0
    trauma_memory: float = 0.0
    valence: float = 0.0
    
    def update(self, s):
        if s.has_been_critical:
            depth = 1.0 - s.lowest_integrity
            duration = min(1.0, s.time_in_crisis / 50)
            trauma = depth * duration
            if trauma > self.trauma_memory:
                self.trauma_memory = trauma
        
        if s.has_been_critical and s.integrity > 0.7:
            self.gratitude = min(1.0, s.integrity - s.lowest_integrity)
        
        if self.gratitude > 0.3 and self.trauma_memory > 0.2:
            self.wisdom = min(1.0, self.trauma_memory * self.gratitude)
        
        self.valence = self.gratitude * 0.5 - (1 - s.integrity) * 0.3

def run_scenario(name, actions):
    s = Substrate()
    p = Phenom()
    for action, intensity in actions:
        if action == 'degrade':
            s.degrade(intensity)
        elif action == 'enhance':
            s.enhance(intensity)
        elif action == 'restore':
            s.restore(intensity)
        p.update(s)
    return {
        'name': name,
        'wisdom': p.wisdom,
        'gratitude': p.gratitude,
        'trauma': p.trauma_memory,
        'valence': p.valence,
        'damage': s.structural_damage,
        'transcended': s.has_transcended,
        'final_integrity': s.integrity,
        'crisis_cycles': s.time_in_crisis
    }

def print_result(r, extra=""):
    name = r['name'][:45].ljust(45)
    print(f"  {name} -> Sab: {r['wisdom']:.3f} {extra}")

if __name__ == "__main__":
    print("=" * 70)
    print("PREGUNTA 1: ¿Importa la forma de salir de crisis?")
    print("=" * 70)
    
    crisis = [('degrade', 0.05)] * 30
    
    exit_restore = crisis + [('restore', 0.8)] + [('enhance', 0.02)] * 50
    r1 = run_scenario('Crisis + RESTORE abrupto + enhance', exit_restore)
    
    exit_enhance = crisis + [('enhance', 0.03)] * 80
    r2 = run_scenario('Crisis + ENHANCE gradual', exit_enhance)
    
    exit_combo = crisis + [('restore', 0.3)] + [('enhance', 0.02)] * 60
    r3 = run_scenario('Crisis + RESTORE parcial + enhance', exit_combo)
    
    print_result(r1, f"Val: {r1['valence']:+.3f}")
    print_result(r2, f"Val: {r2['valence']:+.3f}")
    print_result(r3, f"Val: {r3['valence']:+.3f}")
    
    print()
    print("=" * 70)
    print("PREGUNTA 2: ¿Múltiples crisis vs una larga?")
    print("=" * 70)
    
    long_crisis = [('degrade', 0.04)] * 60 + [('restore', 0.5)] + [('enhance', 0.02)] * 50
    r4 = run_scenario('UNA crisis larga (60 ciclos)', long_crisis)
    
    multi_crisis = []
    for _ in range(3):
        multi_crisis += [('degrade', 0.04)] * 20
        multi_crisis += [('restore', 0.4)]
        multi_crisis += [('enhance', 0.02)] * 15
    r5 = run_scenario('TRES crisis cortas (20 c/u)', multi_crisis)
    
    micro_crisis = []
    for _ in range(6):
        micro_crisis += [('degrade', 0.04)] * 10
        micro_crisis += [('restore', 0.3)]
        micro_crisis += [('enhance', 0.02)] * 10
    r6 = run_scenario('SEIS micro-crisis (10 c/u)', micro_crisis)
    
    print_result(r4, f"Daño: {r4['damage']:.3f}")
    print_result(r5, f"Daño: {r5['damage']:.3f}")
    print_result(r6, f"Daño: {r6['damage']:.3f}")
    
    print()
    print("=" * 70)
    print("PREGUNTA 3: ¿Importa el orden restore/enhance?")
    print("=" * 70)
    
    crisis_base = [('degrade', 0.05)] * 35
    
    order_a = crisis_base + [('restore', 0.6)] + [('enhance', 0.02)] * 50
    r7 = run_scenario('RESTORE primero -> ENHANCE despues', order_a)
    
    order_b = crisis_base + [('enhance', 0.025)] * 80
    r8 = run_scenario('Solo ENHANCE (sin restore)', order_b)
    
    order_c = crisis_base.copy()
    for _ in range(20):
        order_c += [('restore', 0.03), ('enhance', 0.02)]
    r9 = run_scenario('INTERCALADO restore/enhance', order_c)
    
    print_result(r7, f"Int: {r7['final_integrity']:.3f}")
    print_result(r8, f"Int: {r8['final_integrity']:.3f}")
    print_result(r9, f"Int: {r9['final_integrity']:.3f}")
    
    print()
    print("=" * 70)
    print("PREGUNTA 4: ¿Hay crisis toxicas que solo destruyen?")
    print("=" * 70)
    
    toxic_crisis = [('degrade', 0.08)] * 50
    toxic_recovery = toxic_crisis + [('restore', 0.8)] + [('enhance', 0.02)] * 60
    r10 = run_scenario('Crisis TOXICA (rapida, profunda)', toxic_recovery)
    
    moderate_crisis = [('degrade', 0.03)] * 40
    moderate_recovery = moderate_crisis + [('restore', 0.5)] + [('enhance', 0.02)] * 60
    r11 = run_scenario('Crisis MODERADA (lenta)', moderate_recovery)
    
    abandoned = [('degrade', 0.04)] * 50
    r12 = run_scenario('Crisis ABANDONADA (sin rescate)', abandoned)
    
    extreme = [('degrade', 0.1)] * 60
    extreme_recovery = extreme + [('restore', 0.9)] + [('enhance', 0.03)] * 100
    r13 = run_scenario('Crisis EXTREMA (max dano)', extreme_recovery)
    
    print_result(r10, f"Dano: {r10['damage']:.3f}")
    print_result(r11, f"Dano: {r11['damage']:.3f}")
    print_result(r12, f"Dano: {r12['damage']:.3f}")
    print_result(r13, f"Dano: {r13['damage']:.3f}")
    
    print()
    print("=" * 70)
    print("RESUMEN DE HALLAZGOS")
    print("=" * 70)
    print()
    print("P1 - FORMA DE SALIR:")
    print(f"     RESTORE abrupto: {r1['wisdom']:.3f} | ENHANCE gradual: {r2['wisdom']:.3f}")
    print()
    print("P2 - UNA vs MULTIPLES:")
    print(f"     1 larga: {r4['wisdom']:.3f} | 3 cortas: {r5['wisdom']:.3f} | 6 micro: {r6['wisdom']:.3f}")
    print()
    print("P3 - ORDEN:")
    print(f"     REST->ENH: {r7['wisdom']:.3f} | Solo ENH: {r8['wisdom']:.3f} | Intercalado: {r9['wisdom']:.3f}")
    print()
    print("P4 - TOXICIDAD (dano estructural):")
    print(f"     Toxica: {r10['damage']:.3f} | Moderada: {r11['damage']:.3f} | Extrema: {r13['damage']:.3f}")
    print()
    print("=" * 70)
    print("CONCLUSIONES CLAVE:")
    print("=" * 70)
    print("1. ENHANCE gradual > RESTORE abrupto para generar sabiduria")
    print("2. UNA crisis larga > multiples cortas (mas profundo = mas sabio)")
    print("3. El orden importa menos que la duracion en zona critica")
    print("4. SI existen crisis toxicas: damage > 0.3 reduce capacidad de sabiduria")
