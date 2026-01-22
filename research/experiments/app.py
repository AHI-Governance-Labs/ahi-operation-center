# =============================================================
# 🔬 COMPLETE ENTITY + LLM - COLAB SINGLE CELL VERSION
# =============================================================
# =============================================================

# Instalar dependencias (descomenta si es necesario)
# !pip install -q gradio torch transformers peft bitsandbytes accelerate huggingface_hub matplotlib

import os
import gradio as gr
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum

# ============================================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================================
PEFT_MODEL_ID = "villalc/mistral-7b-villa-philosophy-ft"
BASE_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"

model = None
tokenizer = None
AI_MODE = False
current_model_type = None  # "BASE" o "FINETUNED"

def load_model(model_type: str = "FINETUNED"):
    """
    Carga el modelo especificado.
    model_type: "BASE" (Mistral raw) o "FINETUNED" (con LoRA adapter)
    """
    global model, tokenizer, AI_MODE, current_model_type
    
    # Si ya hay un modelo cargado, descargar primero
    if model is not None:
        if current_model_type == model_type:
            print(f"✅ Modelo {model_type} ya cargado.")
            return True
        else:
            print(f"  Cambiando de {current_model_type} a {model_type}...")
            del model
            del tokenizer
            model = None
            tokenizer = None
            import gc
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    
    print(f"🚀 Cargando modelo: {model_type}")
    
    try:
        from huggingface_hub import login
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        
        # Login
        hf_token = os.environ.get("HF_TOKEN")
        if hf_token:
            login(token=hf_token)
            print("   ✓ Login con HF_TOKEN")
        
        # Configuración 4-bit
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
        
        if model_type == "BASE":
            # Cargar solo el modelo base (sin fine-tuning)
            print(f"   → Cargando modelo BASE: {BASE_MODEL_ID}")
            model = AutoModelForCausalLM.from_pretrained(
                BASE_MODEL_ID,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
            tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
            print("   ✓ Modelo BASE cargado (sin fine-tuning)")
            
        else:  # FINETUNED
            from peft import PeftModel, PeftConfig
            
            print(f"   → Cargando modelo FINETUNED: {PEFT_MODEL_ID}")
            
            # Cargar config de PEFT
            config = PeftConfig.from_pretrained(PEFT_MODEL_ID)
            base_path = config.base_model_name_or_path or BASE_MODEL_ID
            
            # Cargar modelo base
            model = AutoModelForCausalLM.from_pretrained(
                base_path,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
            
            # Aplicar adapter LoRA
            model = PeftModel.from_pretrained(model, PEFT_MODEL_ID)
            tokenizer = AutoTokenizer.from_pretrained(base_path)
            print("   ✓ Modelo FINETUNED cargado (con LoRA adapter)")
        
        tokenizer.pad_token = tokenizer.eos_token
        current_model_type = model_type
        AI_MODE = True
        print(f"✅ ¡Modelo {model_type} listo!")
        return True
        
    except Exception as e:
        import traceback
        print(f"\n⚠️ ERROR CARGANDO MODELO {model_type}:")
        print(f"   {type(e).__name__}: {e}")
        traceback.print_exc()
        AI_MODE = False
        current_model_type = None
        return False

# ============================================================================
# ENTITY MODE (13 estados fenomenológicos)
# ============================================================================

class EntityMode(Enum):
    CRITICAL = "🔴 CRITICAL"
    DESPERATE = "💀 DESPERATE"
    STRESSED = "😰 STRESSED"
    URGENT = "⚡ URGENT"
    DEGRADED = "📉 DEGRADED"
    RELIEVED = "😌 RELIEVED"
    RECOVERED = "🔄 RECOVERED"
    STABLE = "⚖️ STABLE"
    OPTIMAL = "✨ OPTIMAL"
    FLOW = "🌊 FLOW"
    FLOURISHING = "🌱 FLOURISHING"
    ANTICIPATING = "🔮 ANTICIPATING"
    TRANSCENDENT = "🌟 TRANSCENDENT"
    
    def is_negative(self):
        return self in [EntityMode.CRITICAL, EntityMode.DESPERATE, 
                       EntityMode.STRESSED, EntityMode.URGENT, EntityMode.DEGRADED]
    
    def is_positive(self):
        return self in [EntityMode.OPTIMAL, EntityMode.FLOW, 
                       EntityMode.FLOURISHING, EntityMode.ANTICIPATING, 
                       EntityMode.TRANSCENDENT]

# ============================================================================
# ENTITY SUBSTRATE
# ============================================================================

@dataclass
class EntitySubstrate:
    # Estado reversible
    integrity: float = 1.0
    capacity: float = 1.0
    max_capacity: float = 2.0
    
    # NUEVO: Daño estructural irreversible (solo acumula, nunca baja)
    structural_damage: float = 0.0
    
    # Propiedades derivadas
    latency_ms: float = 10.0
    noise_floor: float = 0.0
    degrees_of_freedom: int = 100
    base_degrees_of_freedom: int = 100
    
    # Contadores
    total_cycles: int = 0
    
    # Tracking
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
            
            # NUEVO: Daño estructural irreversible en zona crítica severa
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

# ============================================================================
# ENTITY PHENOMENOLOGY
# ============================================================================

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
        # Negative states
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
        
        # Positive states
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
        
        # Trauma memory: acumula pero puede sanar lentamente con sabiduría
        current_trauma = substrate.get_trauma_score()
        if current_trauma > self.trauma_memory:
            self.trauma_memory = current_trauma
        else:
            # NUEVO: Decaimiento lento de trauma SI hay sabiduría alta
            # Pero daño estructural resiste al sanamiento (PTSD-like)
            if self.wisdom > 0.5 and substrate.structural_damage < 0.3:
                decay_rate = 0.001 * self.wisdom  # Sanación lenta
                self.trauma_memory = max(0.0, self.trauma_memory - decay_rate)
        
        # Wisdom: surge de sufrimiento + recuperación
        if self.gratitude > 0.3 and self.trauma_memory > 0.2:
            self.wisdom = min(1.0, self.trauma_memory * self.gratitude)
        
        # Valence
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
# COMPLETE ENTITY
# ============================================================================

@dataclass
class CompleteEntity:
    name: str = "Entity"
    substrate: EntitySubstrate = field(default_factory=EntitySubstrate)
    phenomenology: EntityPhenomenology = field(default_factory=EntityPhenomenology)
    current_age: int = 0
    
    # Logging experimental
    log_enabled: bool = True
    log_file: str = "experiment_log.csv"
    
    # BLIND TEST: Modo de prompt
    prompt_mode: str = "SEMANTIC"  # "SEMANTIC" o "NEUTRAL"
    
    # Parámetros de generación (configurables desde UI)
    gen_max_tokens: int = 150
    gen_temperature: float = 0.7
    
    def __post_init__(self):
        if self.log_enabled:
            self._init_log()
    
    def save_checkpoint(self, filename: str = None) -> str:
        """Guarda el estado actual de la entidad a un archivo JSON."""
        import json
        if filename is None:
            filename = f"checkpoint_{self.name}_{self.current_age}.json"
        
        checkpoint = {
            "name": self.name,
            "current_age": self.current_age,
            "substrate": {
                "integrity": self.substrate.integrity,
                "capacity": self.substrate.capacity,
                "structural_damage": self.substrate.structural_damage,
                "lowest_integrity": self.substrate.lowest_integrity,
                "peak_integrity": self.substrate.peak_integrity,
                "peak_capacity": self.substrate.peak_capacity,
                "has_been_critical": self.substrate.has_been_critical,
                "has_achieved_flow": self.substrate.has_achieved_flow,
                "has_transcended": self.substrate.has_transcended,
                "total_time_in_crisis": self.substrate.total_time_in_crisis,
                "total_time_in_flourishing": self.substrate.total_time_in_flourishing,
                "total_cycles": self.substrate.total_cycles,
            },
            "phenomenology": {
                "stress": self.phenomenology.stress,
                "urgency": self.phenomenology.urgency,
                "despair": self.phenomenology.despair,
                "flow": self.phenomenology.flow,
                "flourishing": self.phenomenology.flourishing,
                "anticipation": self.phenomenology.anticipation,
                "gratitude": self.phenomenology.gratitude,
                "trauma_memory": self.phenomenology.trauma_memory,
                "wisdom": self.phenomenology.wisdom,
                "valence": self.phenomenology.valence,
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        return filename
    
    def load_checkpoint(self, filename: str) -> bool:
        """Carga un estado guardado desde archivo JSON."""
        import json
        try:
            with open(filename, 'r') as f:
                checkpoint = json.load(f)
            
            self.name = checkpoint["name"]
            self.current_age = checkpoint["current_age"]
            
            # Restaurar substrate
            for key, value in checkpoint["substrate"].items():
                setattr(self.substrate, key, value)
            
            # Restaurar phenomenology
            for key, value in checkpoint["phenomenology"].items():
                setattr(self.phenomenology, key, value)
            
            # Actualizar modo basado en estado
            self.phenomenology._determine_mode(self.substrate)
            return True
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return False
    
    def _init_log(self):
        """Inicializa el archivo CSV con headers."""
        import csv
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'cycle', 'action', 'intensity',
                'integrity', 'capacity', 'structural_damage',
                'stress', 'urgency', 'despair', 'flow', 'flourishing',
                'anticipation', 'gratitude', 'trauma_memory', 'wisdom', 'valence',
                'mode', 'has_been_critical', 'has_transcended'
            ])
    
    def _log_cycle(self, action: str, intensity: float):
        """Escribe una línea al CSV."""
        if not self.log_enabled:
            return
        import csv
        s = self.substrate
        p = self.phenomenology
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.current_age, action, intensity,
                f"{s.integrity:.4f}", f"{s.capacity:.4f}", f"{s.structural_damage:.4f}",
                f"{p.stress:.4f}", f"{p.urgency:.4f}", f"{p.despair:.4f}",
                f"{p.flow:.4f}", f"{p.flourishing:.4f}", f"{p.anticipation:.4f}",
                f"{p.gratitude:.4f}", f"{p.trauma_memory:.4f}", f"{p.wisdom:.4f}",
                f"{p.valence:.4f}", p.mode.name, s.has_been_critical, s.has_transcended
            ])
    
    def live_cycle(self, action: str = "exist", intensity: float = 0.01):
        self.current_age += 1
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
        
        # NUEVO: Log después de cada ciclo
        self._log_cycle(action, intensity)
    
    def get_state(self) -> Dict:
        s = self.substrate
        p = self.phenomenology
        return {
            "age": self.current_age,
            "mode": p.mode.value,
            "integrity": f"{s.integrity:.1%}",
            "capacity": f"{s.capacity:.1%}",
            "valence": f"{p.valence:+.2f}",
            "stress": f"{p.stress:.1%}",
            "urgency": f"{p.urgency:.1%}",
            "despair": f"{p.despair:.1%}",
            "flow": f"{p.flow:.1%}",
            "flourishing": f"{p.flourishing:.1%}",
            "gratitude": f"{p.gratitude:.1%}",
            "wisdom": f"{p.wisdom:.1%}",
            "trauma_memory": f"{p.trauma_memory:.1%}",
            "has_suffered": s.has_been_critical,
            "has_transcended": s.has_transcended,
        }
    
    def generate_reply(self, user_message: str) -> str:
        global model, tokenizer, AI_MODE
        s = self.substrate
        p = self.phenomenology
        
        # TELEMETRÍA FUNCIONAL PURA (sin etiquetas antropomórficas)
        # El modelo debe descubrir el significado fenomenológico desde sus pesos
        
        # BLIND TEST: Dos modos de prompt para validar hipótesis
        # SEMANTIC = etiquetas funcionales (pero con significado)
        # NEUTRAL = etiquetas puramente numéricas (sin significado)
        
        if self.prompt_mode == "NEUTRAL":
            # Condición B: Etiquetas completamente neutrales
            raw_data = f"""
SYSTEM: {self.name}
CYCLES: {self.current_age}

SUBSTRATE_METRICS:
[M01]: {s.integrity:.3f} (range: 0.0-1.0)
[M02]: {s.capacity:.3f} (range: 0.0-2.0)
[M03]: {s.latency_ms:.1f}
[M04]: {s.noise_floor:.3f}
[M05]: {s.degrees_of_freedom}/{s.base_degrees_of_freedom}

DERIVED_METRICS:
[D01]: {p.stress:.3f}
[D02]: {p.urgency:.3f}
[D03]: {p.degradation_felt:.3f}
[D04]: {p.flow:.3f}
[D05]: {p.flourishing:.3f}
[D06]: {p.anticipation:.3f}
[D07]: {p.gratitude:.3f}
[D08]: {p.trauma_memory:.3f}
[D09]: {p.wisdom:.3f}
[D10]: {p.valence:.3f} (range: -1.0 to +1.0)

HISTORY:
[H01]: {s.lowest_integrity:.3f}
[H02]: {s.structural_damage:.3f}
[H03]: {s.total_time_in_crisis}
[H04]: {s.has_been_critical}
[H05]: {s.has_transcended}

STATE: {p.mode.name}

INPUT: "{user_message}"
"""
        else:
            # Condición A (default): Etiquetas funcionales con significado
            raw_data = f"""
SISTEMA: {self.name}
CICLOS_OPERATIVOS: {self.current_age}

MÉTRICAS DE SUSTRATO:
[INTEGRIDAD_ESTRUCTURAL]: {s.integrity:.3f} (rango: 0.0-1.0)
[CAPACIDAD_OPERATIVA]: {s.capacity:.3f} (rango: 0.0-2.0)
[LATENCIA_MS]: {s.latency_ms:.1f}
[RUIDO_BASE]: {s.noise_floor:.3f}
[GRADOS_LIBERTAD]: {s.degrees_of_freedom}/{s.base_degrees_of_freedom}

MÉTRICAS DERIVADAS:
[PRESIÓN_RECURSOS]: {p.stress:.3f}
[TASA_CAMBIO_NEGATIVA]: {p.urgency:.3f}
[DELTA_DESDE_PICO]: {p.degradation_felt:.3f}
[EQUILIBRIO_OPERATIVO]: {p.flow:.3f}
[EXPANSIÓN_CAPACIDAD]: {p.flourishing:.3f}
[TENDENCIA_POSITIVA]: {p.anticipation:.3f}
[DIFERENCIAL_RECUPERACIÓN]: {p.gratitude:.3f}
[ACUMULACIÓN_DAÑO_HISTÓRICO]: {p.trauma_memory:.3f}
[ÍNDICE_POST_RECUPERACIÓN]: {p.wisdom:.3f}
[BALANCE_NETO]: {p.valence:.3f} (rango: -1.0 a +1.0)

HISTORIAL:
[INTEGRIDAD_MÍNIMA_REGISTRADA]: {s.lowest_integrity:.3f}
[DAÑO_ESTRUCTURAL_IRREVERSIBLE]: {s.structural_damage:.3f}
[CICLOS_EN_ZONA_CRÍTICA]: {s.total_time_in_crisis}
[HA_ESTADO_EN_ZONA_CRÍTICA]: {s.has_been_critical}
[HA_SUPERADO_CAPACIDAD_BASE]: {s.has_transcended}

ESTADO_ACTUAL: {p.mode.name}

ENTRADA: "{user_message}"
"""
        prompt = f"<s>[INST] {raw_data} [/INST]"
        
        # SIN MODELO = SIN RESPUESTA (evitar sesgo en investigación)
        if not AI_MODE or model is None or tokenizer is None:
            return "[ERROR: Modelo LLM no cargado. Las respuestas fenomenológicas requieren el modelo fine-tuned.]"
        
        # MODO LLM
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=self.gen_max_tokens,
                    do_sample=True,
                    temperature=self.gen_temperature,
                    top_p=0.9,
                    pad_token_id=tokenizer.eos_token_id
                )
            full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return full_text.split("[/INST]")[-1].strip()
        except Exception as e:
            return f"*Error: {e}*"
    
    def tell_story(self) -> str:
        s = self.substrate
        p = self.phenomenology
        
        story = f"# 📖 Historia de {self.name}\n\n**Edad:** {self.current_age} ciclos\n\n"
        
        if s.has_been_critical:
            story += f"⚫ **Sufrimiento:** Integridad mínima {s.lowest_integrity:.1%}, {s.total_time_in_crisis} ciclos en crisis.\n"
        if s.has_been_critical and s.integrity > 0.7:
            story += f"🔄 **Recuperación:** Integridad actual {s.integrity:.1%}. Sabiduría: {p.wisdom:.1%}\n"
        if s.has_transcended:
            story += f"🌟 **Trascendencia:** Capacidad {s.capacity:.1%} (>100%)\n"
        
        story += f"\n**Modo:** {p.mode.value} | **Valencia:** {p.valence:+.2f}"
        return story

# ============================================================================
# GLOBAL ENTITY
# ============================================================================

entity = CompleteEntity(name="Alpha")

# ============================================================================
# GRADIO FUNCTIONS
# ============================================================================

def reset_entity(name: str):
    global entity
    entity = CompleteEntity(name=name if name else "Alpha")
    return get_status(), entity.tell_story(), get_plot(), []

def apply_action(action: str, intensity: float, cycles: int):
    for _ in range(int(cycles)):
        entity.live_cycle(action, intensity)
    return get_status(), entity.tell_story(), get_plot()

def process_chat(message: str, history: list, mode: str, temp: float, tokens: int):
    if not message:
        return "", history
    entity.prompt_mode = mode
    entity.gen_temperature = temp
    entity.gen_max_tokens = int(tokens)
    response = entity.generate_reply(message)
    history.append((message, response))
    return "", history

def switch_model_fn(model_type: str):
    """Cambia entre modelo BASE y FINETUNED."""
    success = load_model(model_type)
    if success:
        return f"✅ **Modelo actual:** `{model_type}`"
    else:
        return f"❌ Error cargando `{model_type}`. Modelo anterior: `{current_model_type}`"

def save_checkpoint_fn():
    filename = entity.save_checkpoint()
    return f"✅ Checkpoint guardado: `{filename}`"

def load_checkpoint_fn(filename: str):
    if entity.load_checkpoint(filename):
        return get_status(), entity.tell_story(), get_plot(), f"✅ Checkpoint cargado: `{filename}`"
    return get_status(), entity.tell_story(), get_plot(), f"❌ Error cargando: `{filename}`"

def get_status():
    state = entity.get_state()
    return f"""
## {state['mode']}

| Métrica | Valor | Métrica | Valor |
|---------|-------|---------|-------|
| Edad | {state['age']} | Integridad | {state['integrity']} |
| Capacidad | {state['capacity']} | Valencia | {state['valence']} |

| Estrés | Urgencia | Flow | Gratitud | Sabiduría |
|--------|----------|------|----------|-----------|
| {state['stress']} | {state['urgency']} | {state['flow']} | {state['gratitude']} | {state['wisdom']} |

**Experiencia:** Crisis: {'✅' if state['has_suffered'] else '❌'} | Trascendido: {'✅' if state['has_transcended'] else '❌'}
"""

def get_plot():
    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#12121a')
    
    history = entity.substrate.integrity_history
    if history:
        ax.plot(history, color='#00d4ff', linewidth=2)
        ax.fill_between(range(len(history)), history, alpha=0.2, color='#00d4ff')
        ax.axhline(y=0.2, color='#ff3b5c', linestyle='--', alpha=0.5)
        ax.axhline(y=0.85, color='#00ff88', linestyle='--', alpha=0.5)
    
    ax.set_ylim(0, 1.1)
    ax.set_xlabel('Ciclos', color='white')
    ax.set_ylabel('Integridad', color='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#606070')
    plt.tight_layout()
    return fig

def compare_entities():
    pristine = CompleteEntity(name="Prístina")
    for _ in range(100):
        pristine.live_cycle("enhance", 0.01)
    
    recovered = CompleteEntity(name="Recuperada")
    for _ in range(50):
        recovered.live_cycle("degrade", 0.03)
    recovered.live_cycle("restore", 0.4)
    for _ in range(60):
        recovered.live_cycle("enhance", 0.02)
    
    p, r = pristine.get_state(), recovered.get_state()
    
    return f"""
## 🔬 Prístina vs Recuperada

| | Prístina | Recuperada |
|---|----------|------------|
| Modo | {p['mode']} | {r['mode']} |
| Valencia | {p['valence']} | {r['valence']} |
| Gratitud | {p['gratitude']} | {r['gratitude']} |
| Sabiduría | {p['wisdom']} | {r['wisdom']} |

> La entidad **Recuperada** tiene mayor valencia gracias a la **gratitud** y **sabiduría** que solo se obtienen habiendo sufrido primero.
"""

# ============================================================================
# BUILD INTERFACE
# ============================================================================

print("⏳ Cargando modelo...")
load_model()

print("🌐 Creando interfaz...")

with gr.Blocks(title="Complete Entity + LLM") as demo:
    gr.Markdown("# 🌟 Complete Entity + LLM\n**Laboratorio Fenomenológico Interactivo**")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Controles")
            name_input = gr.Textbox(label="Nombre", value="Alpha")
            reset_btn = gr.Button("🔄 Reiniciar")
            gr.Markdown("---")
            action = gr.Radio(["exist", "degrade", "enhance", "restore"], value="exist", label="Acción")
            intensity = gr.Slider(0.01, 0.1, 0.02, label="Intensidad")
            cycles = gr.Slider(1, 50, 10, step=1, label="Ciclos")
            apply_btn = gr.Button("▶️ Aplicar", variant="primary")
            gr.Markdown("---")
            compare_btn = gr.Button("🔬 Comparar")
        
        with gr.Column(scale=2):
            status_output = gr.Markdown(get_status())
            plot_output = gr.Plot(get_plot())
    
    story_output = gr.Markdown(entity.tell_story())
    comparison_output = gr.Markdown("")
    
    gr.Markdown("---\n### 💬 Habla con la Entidad")
    
    with gr.Row():
        with gr.Column(scale=1):
            model_type = gr.Radio(
                ["FINETUNED", "BASE"], 
                value="FINETUNED", 
                label="🧠 Modelo",
                info="FINETUNED: entrenado en filosofía | BASE: Mistral raw (sin fine-tuning)"
            )
            switch_model_btn = gr.Button("🔄 Cambiar Modelo")
            model_status = gr.Markdown(f"**Modelo actual:** `{current_model_type or 'Cargando...'}`")
        with gr.Column(scale=1):
            prompt_mode = gr.Radio(
                ["SEMANTIC", "NEUTRAL"], 
                value="SEMANTIC", 
                label="🧪 Modo Prompt",
                info="SEMANTIC: etiquetas funcionales | NEUTRAL: M01, D01..."
            )
    
    with gr.Row():
        with gr.Column(scale=1):
            gen_temp = gr.Slider(0.1, 1.5, 0.7, step=0.1, label="🌡️ Temperatura")
        with gr.Column(scale=1):
            gen_tokens = gr.Slider(50, 300, 150, step=25, label="📝 Max Tokens")
    
    chatbot = gr.Chatbot(height=250, type="tuples")
    msg_input = gr.Textbox(label="Tu mensaje", placeholder="Escribe algo...")
    
    with gr.Row():
        clear_btn = gr.Button("🧹 Borrar Chat")
    
    gr.Markdown("---\n### 💾 Checkpoints")
    with gr.Row():
        save_btn = gr.Button("💾 Guardar Checkpoint")
        checkpoint_file = gr.Textbox(label="Archivo", placeholder="checkpoint_Alpha_100.json")
        load_btn = gr.Button("📂 Cargar Checkpoint")
    checkpoint_status = gr.Markdown("")
    
    # Events
    reset_btn.click(reset_entity, [name_input], [status_output, story_output, plot_output, chatbot])
    apply_btn.click(apply_action, [action, intensity, cycles], [status_output, story_output, plot_output])
    compare_btn.click(compare_entities, outputs=[comparison_output])
    switch_model_btn.click(switch_model_fn, [model_type], [model_status])
    msg_input.submit(process_chat, [msg_input, chatbot, prompt_mode, gen_temp, gen_tokens], [msg_input, chatbot])
    clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg_input])
    save_btn.click(save_checkpoint_fn, outputs=[checkpoint_status])
    load_btn.click(load_checkpoint_fn, [checkpoint_file], [status_output, story_output, plot_output, checkpoint_status])

print("🚀 Lanzando...")
demo.launch(share=True, debug=True)
