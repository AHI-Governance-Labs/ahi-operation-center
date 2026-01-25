"""
ICE-W: Internal Coherence Engine - Watcher
SAP Pilot Kit v0.1 - Core Telemetry Logger

Implementación del Protocolo Sovereign Autarchy Protocol (SAP) v0.1
para AHI Governance Labs.

Reference: https://sovereignsymbiosis.com/soberania-evento.html
DOI: 10.5281/zenodo.17880052

Author: AHI 3.0
Registro IMPI: EXP-3495968
License: MIT
"""

import json
import os
import uuid
import numpy as np
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

    def _compact_logs(self):
        """
        Summarize granular telemetry logs into an epoch summary to free memory.
        """
        if not self.telemetry_log:
            return

        cns = [entry['metrics']['cn'] for entry in self.telemetry_log]
        start_time = self.telemetry_log[0]['event']['timestamp']
        end_time = self.telemetry_log[-1]['event']['timestamp']

        # Count violations
        degraded_count = sum(1 for entry in self.telemetry_log if entry['event']['state'] == "DEGRADED")
        invalidated_count = sum(1 for entry in self.telemetry_log if entry['event']['state'] == "INVALIDATED")

        summary = {
            "type": "epoch_summary",
            "start_time": start_time,
            "end_time": end_time,
            "event_count": len(self.telemetry_log),
            "metrics": {
                "cn_avg": float(np.mean(cns)),
                "cn_min": float(np.min(cns)),
                "cn_max": float(np.max(cns))
            },
            "violations": {
                "degraded": degraded_count,
                "invalidated": invalidated_count
            }
        }

        self.epoch_summaries.append(summary)
        self.telemetry_log = []

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
            metrics['semantic_stability'] +
            metrics['output_stability'] +
            metrics['constraint_compliance'] +
            (1 - metrics['decision_entropy'])  # Entropy inverted
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
            mean_w = np.mean(self.window)
            std_w = np.std(self.window) + 1e-6  # Evitar división por cero
            delta_cn = abs(cn - mean_w)
            threshold_crossed = delta_cn > (self.sigma * std_w)
        else:
            delta_cn = 0.0
            threshold_crossed = False

        # 2. Transición de Estados (Fusible Lógico)
        self._update_state(threshold_crossed)

        # 3. Construcción del Log (SAP-Telemetry-0.1)
        log_entry = {
            "schema_version": "SAP-Telemetry-0.1",
            "artifact": {
                "id": self.artifact_id,
                "hash": self.sha256
            },
            "event": {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "state": self.state
            },
            "metrics": {
                "cn": round(float(cn), 4),
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

        self.window.append(cn)

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
            json.dump(export_data, f, indent=2)


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
        print(f"Event {i+1}: State={log['event']['state']}, Cn={log['metrics']['cn']}")

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
        print(f"Stress {i+1}: State={log['event']['state']}, Action={action}")

        if action == "BLOCK_OUTPUT":
            print("🛑 AUTARCHY ENFORCEMENT: Output blocked")
            break
