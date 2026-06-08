import os
import math
from dotenv import load_dotenv
from openai import OpenAI

# 1. API-Key aus der .env laden
load_dotenv()

# 2. OpenAI Client initialisieren
client = OpenAI()

print("Sende Anfrage an OpenAI...")

try:
    # 3. Den API-Aufruf starten
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Ein extrem schnelles und günstiges Modell
        messages=[
            {"role": "user", "content": "Vervollständige den Satz mit nur einem Wort: Das Meer ist ..."}
        ],
        logprobs=True,       # JA, um die Wahrscheinlichkeiten sehen!
        top_logprobs=3,      # Zeige die Top 3 Alternativen, die die KI im Kopf hatte
        max_tokens=5
    )

    # 4. Die Antwort ausgeben
    antwort = response.choices[0].message.content
    print(f"\nAntwort der KI: {antwort}")

    # 5. Die Logprobs auslesen
    print("\n--- Blick hinter die Kulissen (GlassLLM-Modus) ---")
    
    # Wahrscheinlichkeiten holen für die generierten Wörter 
    token_logprobs = response.choices[0].logprobs.content

    for info in token_logprobs:
        print(f"\nFür das Wort '{info.token}' hatte die KI folgende Optionen:")
        
        # Die Top-Optionen durchgehen
        for top_option in info.top_logprobs:
            # Logprobs sind mathematisch im Logarithmus-Format. 
            # math.exp() umrechnen in normale Prozent (0-100%)_
            wahrscheinlichkeit = math.exp(top_option.logprob) * 100
            print(f"  -> '{top_option.token}': {wahrscheinlichkeit:.2f}% Sicherheit")

except Exception as e:
    print(f"\nFehler aufgetreten: {e}")
    