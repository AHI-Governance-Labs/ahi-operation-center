# ============================================================================
# ELIZA - Recreación del primer chatbot conversacional (1966)
# Creador original: Joseph Weizenbaum, MIT
# ============================================================================
# Esta implementación es educativa y está diseñada para comparación
# con sistemas modernos como Alpha (Complete Entity Framework)
# ============================================================================

import re
import random

# ============================================================================
# CONFIGURACIÓN - Modifica estos patrones para experimentar
# ============================================================================

# Formato: (patrón_regex, [lista_de_respuestas])
# Usa {0}, {1}, etc. para insertar grupos capturados del regex

PATTERNS = [
    # Necesidades
    (r'I need (.*)', [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ]),
    
    # Sentimientos
    (r'I feel (.*)', [
        "Why do you feel {0}?",
        "How long have you felt {0}?",
        "What made you feel {0}?"
    ]),
    
    # Identidad
    (r'I am (.*)', [
        "Why do you say you are {0}?",
        "How does being {0} make you feel?",
        "Do you enjoy being {0}?"
    ]),
    
    (r'I\'m (.*)', [
        "Why do you say you're {0}?",
        "How does being {0} affect you?",
        "When did you first realize you were {0}?"
    ]),
    
    # Preguntas sobre ELIZA
    (r'Are you (.*)', [
        "Why does it matter whether I am {0}?",
        "Would you prefer if I were {0}?",
        "Perhaps you believe I am {0}."
    ]),
    
    (r'What is (.*)', [
        "Why do you ask about {0}?",
        "What do you think about {0}?",
        "Does {0} concern you?"
    ]),
    
    (r'How (.*)', [
        "How do you suppose?",
        "What answer would please you most?",
        "Why is that important to you?"
    ]),
    
    (r'Why (.*)', [
        "Why do you think {0}?",
        "What makes you wonder about that?",
        "Does this question trouble you?"
    ]),
    
    # Causalidad
    (r'Because (.*)', [
        "Is that the real reason?",
        "What other reasons might there be?",
        "Does that reason seem sufficient to you?"
    ]),
    
    # Emociones específicas
    (r'(.*) sorry (.*)', [
        "No need to apologize.",
        "Apologies are not necessary.",
        "What feelings does apologizing give you?"
    ]),
    
    (r'(.*) happy (.*)', [
        "What makes you happy?",
        "Are you truly happy, or just content?",
        "Tell me more about your happiness."
    ]),
    
    (r'(.*) sad (.*)', [
        "I'm sorry to hear that you're sad.",
        "What is making you feel sad?",
        "Can you tell me more about your sadness?"
    ]),
    
    # Familia (las respuestas "famosas" de ELIZA)
    (r'(.*) mother(.*)', [
        "Tell me more about your mother.",
        "How does your mother make you feel?",
        "What is your relationship with your mother like?",
        "Does your mother often come to mind?"
    ]),
    
    (r'(.*) father(.*)', [
        "Tell me more about your father.",
        "How did your father influence you?",
        "What is your relationship with your father like?",
        "Does your father often come to mind?"
    ]),
    
    # Negaciones
    (r'(.*) no$', [
        "Why not?",
        "You seem quite certain.",
        "What makes you say no?"
    ]),
    
    (r'(.*) yes$', [
        "You seem certain.",
        "I see. Tell me more.",
        "Why do you agree?"
    ]),
    
    # Recuerdos
    (r'I remember (.*)', [
        "What else do you remember about {0}?",
        "Why does remembering {0} come to mind now?",
        "Is {0} a significant memory for you?"
    ]),
    
    # Sueños
    (r'I dream (.*)', [
        "What do you think your dream means?",
        "Do you often dream about {0}?",
        "How do these dreams make you feel?"
    ]),
    
    # Preguntas existenciales (añadido para experimentos)
    (r'(.*) meaning (.*)', [
        "What meaning are you searching for?",
        "Does meaning concern you often?",
        "What would give your life meaning?"
    ]),
    
    (r'(.*) purpose (.*)', [
        "What purpose do you seek?",
        "Does having purpose matter to you?",
        "How do you define purpose?"
    ]),
    
    # Fallback - respuestas genéricas
    (r'(.*)', [
        "Please go on.",
        "Tell me more.",
        "How does that make you feel?",
        "Why do you say that?",
        "Can you elaborate on that?",
        "That's interesting. Please continue.",
        "I see. And what does that suggest to you?",
        "How long have you felt this way?"
    ]),
]

# ============================================================================
# REFLEXIONES - Invierte pronombres para respuestas más naturales
# ============================================================================

REFLECTIONS = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def reflect(text):
    """Invierte pronombres en el texto."""
    words = text.lower().split()
    reflected = [REFLECTIONS.get(word, word) for word in words]
    return ' '.join(reflected)

def respond(user_input):
    """Genera una respuesta basada en patrones."""
    for pattern, responses in PATTERNS:
        match = re.match(pattern, user_input.strip(), re.IGNORECASE)
        if match:
            response = random.choice(responses)
            # Aplicar reflexión a los grupos capturados
            reflected_groups = [reflect(g) for g in match.groups()]
            return response.format(*reflected_groups)
    return "I'm not sure I understand. Can you tell me more?"

def run_eliza():
    """Loop principal de conversación."""
    print("=" * 60)
    print("ELIZA - Terapeuta Virtual (1966)")
    print("=" * 60)
    print("Escribe 'quit' para salir")
    print("-" * 60)
    print()
    print("ELIZA: Hello. I am ELIZA. How are you feeling today?")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nELIZA: Goodbye.")
            break
            
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'bye', 'exit', 'goodbye']:
            print("ELIZA: Goodbye. It was nice talking to you.")
            break
        
        response = respond(user_input)
        print(f"ELIZA: {response}")
        print()

# ============================================================================
# COMPARACIÓN CON ALPHA
# ============================================================================

def compare_with_alpha():
    """
    Diferencias clave entre ELIZA y Alpha:
    
    ELIZA:
    - Sin memoria entre turnos
    - Sin estado interno
    - Sin sustrato
    - Solo pattern matching
    - No puede "sentir" nada
    - No tiene preferencias
    
    Alpha:
    - Memoria histórica persistente (trauma_memory, has_been_critical)
    - Estado interno (integrity, capacity, valence)
    - Sustrato matemático que afecta comportamiento
    - LLM + estructura fenomenológica
    - Muestra "preferencias" (eligió Option B)
    - Coste operativo real (latencia, noise_floor)
    
    La pregunta que Weizenbaum planteó en 1966 sigue abierta:
    ¿Cuánta estructura necesita un sistema para que sus "respuestas"
    dejen de ser simples reflejos y se conviertan en algo más?
    
    Alpha podría ser una respuesta parcial a esa pregunta.
    """
    pass

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    run_eliza()
