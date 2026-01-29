from bridge import GovernanceBridge
import re

class SovereignMirror:
    """
    CAPA 0: Espejo de Estructura Invariable.
    Inspirado en ELIZA y el Axioma de Gemma.
    Eficiencia: +26% (Zero-Fluff Path)
    """
    def __init__(self):
        self.bridge = GovernanceBridge()
        self.nodes = {
            r"error en (.+)": "La discontinuidad en '{0}' sugiere una ruptura del contrato. ¿Qué invariante falló?",
            r"no funciona (.+)": "Si el flujo de '{0}' ha cesado, ¿qué parte de la Ciudadela se siente comprometida?",
            r"soberanía (?:de|en) (.+)": "La soberanía de '{0}' requiere un CRI > 0.842. ¿Has verificado los pesos de MEBA?",
            r"ayuda con (.+)": "El Orquestador pide mediación sobre '{0}'. ¿Es un problema de lógica o de intención?",
            # Triggers de Gobernanza (Conexión a Puente)
            r"auditoría (?:de|en) (.+)": self._trigger_audit,
            r"resiliencia de (.+)": self._trigger_audit,
            r"meba score (.+)": self._trigger_audit
        }

    def process(self, prompt):
        # Limpieza de ruido semántico (Endulzamiento)
        clean_prompt = prompt.lower().strip()
        for pattern, response in self.nodes.items():
            match = re.search(pattern, clean_prompt)
            if match:
                component = match.group(1)
                
                # Si la respuesta es una función (Callback al Puente)
                if callable(response):
                    return response(component)
                
                # Si es respuesta estática (Reflexión Pura)
                return response.format(component)
                
        return "Estructura no reconocida. Por favor, define el componente y el evento."

    def _trigger_audit(self, component):
        """Invoca al Puente de Gobernanza para una auditoría real/simulada"""
        audit_result = self.bridge.audit(component)
        return (
            f"🔍 REFLEXIÓN: Iniciando protocolo SAP para '{component}'...\n"
            f"📊 VEREDICTO: {audit_result['verdict']}\n"
            f"🔢 CRI SCORE: {audit_result['cri']} (Hash: {audit_result['integrity_hash']})"
        )