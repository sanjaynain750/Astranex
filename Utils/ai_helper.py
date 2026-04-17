import os
import requests
from utils.logger import Logger

log = Logger("AI")

def ask_ai(prompt, local=False):
    if local:
        # Ollama API
        try:
            r = requests.post("http://localhost:11434/api/generate",
                              json={"model": "llama3.1:8b", "prompt": prompt, "stream": False})
            return r.json().get("response", "")
        except:
            log.error("Ollama not running. Start with: ollama serve")
            return ""
    else:
        # यहाँ OpenAI या अन्य API का उपयोग कर सकते हैं
        log.warning("AI API not configured. Use --local for offline AI.")
        return ""
