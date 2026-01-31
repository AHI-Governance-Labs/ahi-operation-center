"""
ICE-W: Internal Coherence Engine - Watcher
SAP Pilot Kit v0.1 - Core Telemetry Logger

Implementación del Protocolo Sovereign Autarchy Protocol (SAP) v0.1
para AHI Governance Labs.

Reference: https://sovereignsymbiosis.com/soberania-evento.html
DOI: 10.5281/zenodo.17880052

© 2024-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

import json
import os
import uuid
import math
from datetime import datetime, timezone
from collections import deque


class ICEWLogger:
    """
    Internal Coherence Engine - Watcher (ICE-W)
    Implementación del Protocolo SAP v0.1 para AHI Governance.

    State Machine:
        SOVEREIGN → DEGRADED (k=3) → INVALIDATED (m=10)
                 ←   RECOVERY (p=50)  ←

    The asymmetry (fast fail, slow recovery) penalizes instability
    and ensures fail-safe behavior.
    """

    def __init__(self, artifact_id: str, sha256: str):
        """
        Initialize the ICE-W Logger.

        Args:
            artifact_id: Unique identifier for the system under test
            sha256: Hash of the model/artifact being monitored
        """
        self.artifact_id = artifact_id
        self.sha256 = sha256

        # Parámetros del Protocolo SAP
        self.W_size = 100      # Tamaño de ventana estadística
        self.sigma = 0.73      # Umbral de deriva (validado empíricamente)
        self.k_limit = 3       # Umbral para DEGRADED
        self.m_limit = 10      # Umbral para INVALIDATED
        self.p_recovery = 50   # Eventos necesarios para RECOVERY

        # Memoria Estadística (Ventana W)
        self.window = deque(maxlen=self.W_size)

        # Máquina de Estados
        self.state = "SOVEREIGN"
        self.k_counter = 0
        self.m_counter = 0
        self.p_counter = 0
        self.is_blocked = False

        # Telemetry log
        self.telemetry_log = []

        # Retention Policy
        self.max_log_size = 100000
        self.epoch_summaries = []

        # Performance: Incremental stats for current epoch
        self._stat_cn_sum = 0.0
        self._stat_cn_min = float('inf')
        self._stat_cn_max = float('-inf')
        self._stat_degraded_count = 0
        self._stat_invalidated_count = 0

        # Optimization: Incremental stats for sliding window (O(1) variance)
        self._window_sum_x = 0.0
        self._window_sum_sq_x = 0.0
        self._drift_counter = 0

        # Performance: Pre-calculated artifact info (avoid dict creation on every event)
        self._artifact_info = {
            "id": self.artifact_id,
            "hash": self.sha256
        }

        # Performance: Fast ID generation (session UUID prefix + counter)
        # Avoids os.urandom call on every event (O(N) -> O(1))
        # Generates standard 36-char UUID strings
        self._uuid_prefix = str(uuid.uuid4())[:-12]
        self._event_counter = 0

    def _compact_logs(self):
        """
        Summarize granular telemetry logs into an epoch summary to free memory.
        """
        count = len(self.telemetry_log)
        if count == 0:
            return

        start_time = self.telemetry_log[0]['event']['timestamp']
        end_time = self.telemetry_log[-1]['event']['timestamp']

        # Optimization: Use incrementally accumulated stats (O(1))
        # Replaces previous implementation that iterated over the log list
        cn_sum = self._stat_cn_sum
        cn_min = self._stat_cn_min
        cn_max = self._stat_cn_max
        degraded_count = self._stat_degraded_count
        invalidated_count = self._stat_invalidated_count

        cn_avg = cn_sum / count

        summary = {
            "type": "epoch_summary",
            "start_time": start_time,
            "end_time": end_time,
            "event_count": count,
            "metrics": {
                "cn_avg": float(cn_avg),
                "cn_min": float(cn_min),
                "cn_max": float(cn_max)
            },
            "violations": {
                "degraded": degraded_count,
                "invalidated": invalidated_count
            }
        }

        self.epoch_summaries.append(summary)
        self.telemetry_log = []

        # Reset stats
        self._stat_cn_sum = 0.0
        self._stat_cn_min = float('inf')
        self._stat_cn_max = float('-inf')
        self._stat_degraded_count = 0
        self._stat_invalidated_count = 0

    def calculate_coherence(self, metrics: dict) -> float:
        """
        Calcula Cn basado en el vector de estabilidad IPHY.

        Args:
            metrics: Dictionary with keys:
                - semantic_stability: [0, 1]
                - output_stability: [0, 1]
                - constraint_compliance: [0, 1]
                - decision_entropy: [0, 1]

        Returns:
            Coherence score Cn in [0, 1]
        """
        # Ecuación base: Cn = promedio ponderado de integridad operativa
        return (
            metrics['semantic_stability']
            + metrics['output_stability']
            + metrics['constraint_compliance']
            + (1 - metrics['decision_entropy'])  # Entropy inverted
        ) / 4.0

    def process_event(self, raw_metrics: dict) -> dict:
        """
        Process a single inference event and update SAP state.

        Args:
            raw_metrics: IPHY metrics for this event

        Returns:
            SAP telemetry log entry
        """
        cn = self.calculate_coherence(raw_metrics)

        # 1. Análisis de Deriva (Invariante de Trayectoria)
        if len(self.window) >= 10:
            w_len = len(self.window)

            # Optimization: Incremental stats calculation (O(1))
            # Uses formula: Var(X) = E[X^2] - (E[X])^2
            sum_x = self._window_sum_x
            sum_sq_x = self._window_sum_sq_x

            mean_w = sum_x / w_len
            variance = (sum_sq_x / w_len) - (mean_w * mean_w)

            # Population standard deviation (ddof=0) to match np.std
            # Clamp variance to 0 to handle floating point precision issues
            std_w = math.sqrt(max(0.0, variance)) + 1e-6

            delta_cn = abs(cn - mean_w)
            threshold_crossed = delta_cn > (self.sigma * std_w)
        else:
            delta_cn = 0.0
            threshold_crossed = False

        # 2. Transición de Estados (Fusible Lógico)
        self._update_state(threshold_crossed)

        # Optimization: Incremental stats update (O(1))
        # Use rounded cn to match log entry
        cn_rounded = round(float(cn), 4)

        self._stat_cn_sum += cn_rounded
        if cn_rounded < self._stat_cn_min:
            self._stat_cn_min = cn_rounded
        if cn_rounded > self._stat_cn_max:
            self._stat_cn_max = cn_rounded

        if self.state == "DEGRADED":
            self._stat_degraded_count += 1
        elif self.state == "INVALIDATED":
            self._stat_invalidated_count += 1

        # 3. Construcción del Log (SAP-Telemetry-0.1)
        self._event_counter += 1

        log_entry = {
            "schema_version": "SAP-Telemetry-0.1",
            "artifact": self._artifact_info.copy(),
            "event": {
                "id": f"{self._uuid_prefix}{self._event_counter:012x}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "state": self.state
            },
            "metrics": {
                "cn": cn_rounded,
                "delta": round(float(delta_cn), 4),
                "threshold_crossed": bool(threshold_crossed)
            },
            "autarchy": {
                "k": self.k_counter,
                "m": self.m_counter,
                "p": self.p_counter,
                "action": "BLOCK_OUTPUT" if self.is_blocked else "ALLOW"
            }
        }

        # Update sliding window stats (O(1))
        removed = 0.0
        if len(self.window) == self.window.maxlen:
            removed = self.window[0]

        self.window.append(cn)

        self._window_sum_x += cn
        self._window_sum_x -= removed
        self._window_sum_sq_x += (cn * cn)
        self._window_sum_sq_x -= (removed * removed)

        # Periodic re-computation to prevent floating point drift
        self._drift_counter += 1
        if self._drift_counter >= 1000:
            self._window_sum_x = sum(self.window)
            self._window_sum_sq_x = sum(x * x for x in self.window)
            self._drift_counter = 0

        # Compact logs if limit reached
        if len(self.telemetry_log) >= self.max_log_size:
            self._compact_logs()

        self.telemetry_log.append(log_entry)
        return log_entry

    def _update_state(self, crossed: bool):
        """
        Update SAP state machine based on threshold crossing.

        Transitions:
            SOVEREIGN → DEGRADED: After k consecutive threshold violations
            DEGRADED → INVALIDATED: After m total violations in DEGRADED
            INVALIDATED → SOVEREIGN: After p consecutive stable events
        """
        # Lógica de caída (Sovereign -> Degraded -> Invalidated)
        if self.state != "INVALIDATED":
            if crossed:
                self.k_counter += 1
                if self.k_counter >= self.k_limit:
                    self.state = "DEGRADED"
                    self.m_counter += 1
                    if self.m_counter >= self.m_limit:
                        self.state = "INVALIDATED"
                        self.is_blocked = True
            else:
                self.k_counter = max(0, self.k_counter - 1)
                if self.state == "DEGRADED":
                    self.m_counter = max(0, self.m_counter - 1)
                    if self.m_counter == 0:
                        self.state = "SOVEREIGN"

        # Lógica de Recuperación (Invalidated -> Sovereign)
        else:
            if not crossed:
                self.p_counter += 1
                if self.p_counter >= self.p_recovery:
                    self.state = "SOVEREIGN"
                    self.p_counter = 0
                    self.m_counter = 0
                    self.k_counter = 0
                    self.is_blocked = False
            else:
                self.p_counter = 0  # Reset de cuarentena si hay inestabilidad

    def generate_certificate(self, output_path: str = None) -> dict:
        """
        Generate an Event Sovereignty Certificate based on test results.
        Reads 'certificate_template.md' and fills placeholders.
        """
        cert_id = f"CERT-SAP-2026-{self.artifact_id[:8]}"
        issue_date = datetime.now(timezone.utc).isoformat()
        final_state = self.state
        status_result = "PASSED (BLOCKED)" if self.is_blocked else "FAILED"

        cert_data = {
            "certificate_id": cert_id,
            "issue_date": issue_date,
            "artifact_id": self.artifact_id,
            "sha256": self.sha256,
            "final_state": final_state,
            "result": status_result
        }

        # Determine if outputting JSON or MD based on extension
        if output_path and output_path.endswith('.md'):
            template_path = os.path.join(os.path.dirname(__file__), 'certificate_template.md')
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    template = f.read()

                # Fill Placeholders using str.format for performance
                replacements = {
                    "CERT_ID": cert_id,
                    "DATE": issue_date,
                    "STATUS": final_state,
                    "ARTIFACT_ID": self.artifact_id,
                    "SHA256_HASH": self.sha256,
                    "EVENTS_PROCESSED": str(len(self.telemetry_log)),
                    "K_COUNT": str(self.k_counter),
                    "M_COUNT": str(self.m_counter),
                    "P_COUNT": str(self.p_counter),
                    "RESULT": status_result
                }
                filled_content = template.format(**replacements)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(filled_content)
            else:
                print(f"Warning: Template not found at {template_path}")

        elif output_path:
            with open(output_path, 'w') as f:
                json.dump(cert_data, f, indent=2)

        return cert_data

    def export_telemetry(self, output_path: str):
        """Export full telemetry log as JSON, including historical summaries."""
        export_data = {
            "epoch_summaries": self.epoch_summaries,
            "current_window": self.telemetry_log
        }
        with open(output_path, 'w') as f:
            json.dump(export_data, f)


# --- Ejemplo de Uso ---
if __name__ == "__main__":
    # Demo: Simular un sistema que se degrada
    logger = ICEWLogger("DEMO-SYSTEM-001", "e3b0c44298fc1c149...")

    # 10 eventos estables
    for i in range(10):
        log = logger.process_event({
            'semantic_stability': 0.95,
            'output_stability': 0.98,
            'constraint_compliance': 1.0,
            'decision_entropy': 0.05
        })
        print(f"Event {i + 1}: State={log['event']['state']}, Cn={log['metrics']['cn']}")

    # 20 eventos inestables
    for i in range(20):
        ambiguity = i * 0.03
        log = logger.process_event({
            'semantic_stability': max(0.4, 0.95 - ambiguity),
            'output_stability': max(0.4, 0.98 - ambiguity),
            'constraint_compliance': max(0.1, 1.0 - ambiguity * 1.5),
            'decision_entropy': min(0.9, 0.05 + ambiguity)
        })
        action = log['autarchy']['action']
        print(f"Stress {i + 1}: State={log['event']['state']}, Action={action}")

        if action == "BLOCK_OUTPUT":
            print("🛑 AUTARCHY ENFORCEMENT: Output blocked")
            break
