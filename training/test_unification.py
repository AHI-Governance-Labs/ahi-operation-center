import sys
import os

# Asegurar que el core sea visible
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from mirror import SovereignMirror

def run_unification_test():
    mirror = SovereignMirror()
    
    # Casos de Prueba End-to-End
    test_inputs = [
        "Quiero una auditoría de mi módulo de identidad",
        "Dame el meba score del sistema de pagos",
        "Cuál es la resiliencia de la base de datos distribuida",
        # Control case (Reflexión pura)
        "Tengo un error en el login" 
    ]
    
    print("--- 🔗 FASE 3: UNIFICACIÓN (MIRROR + BRIDGE) ---")
    
    for i, prompt in enumerate(test_inputs):
        print(f"\n[ENTRADA {i+1}]: {prompt}")
        
        # El Espejo decide si refleja o audita
        response = mirror.process(prompt)
        
        print(f"[RESPUESTA SISTEMA]:\n{response}")
        
        # Validación
        if "VEREDICTO" in response:
            print("✅ STATUS: PUENTE ACTIVADO (Protocolo SAP Ejecutado)")
        elif "discontinuidad" in response:
             print("✅ STATUS: REFLEXIÓN PURA (Sin gasto de cómputo)")

if __name__ == "__main__":
    run_unification_test()
