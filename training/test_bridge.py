import sys
import os

# Asegurar que el core sea visible
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from bridge import GovernanceBridge

def run_bridge_test():
    bridge = GovernanceBridge()
    
    test_components = [
        "Modulo de Pagos",
        "Red Neuronal DeepSeek",
        "Contrato Inteligente AHI"
    ]
    
    print(f"--- 🌉 CONECTANDO PUEINTE A SAP ({bridge.sap_version}) ---")
    print(f"--- UMBRAL DE SOBERANÍA: {bridge.meba_threshold} ---\n")
    
    for component in test_components:
        result = bridge.audit(component)
        
        status_icon = "✅" if result["status"] == "SOVEREIGN" else "🛑"
        print(f"{status_icon} COMPONENTE: {result['component']}")
        print(f"   ├─ Hash: {result['integrity_hash']}")
        print(f"   ├─ CRI Score: {result['cri']}")
        print(f"   └─ Veredicto: {result['verdict']}\n")

if __name__ == "__main__":
    run_bridge_test()
