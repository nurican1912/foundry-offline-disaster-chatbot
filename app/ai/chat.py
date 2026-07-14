"""AI Layer — Ollama tabanlı chat (sohbet) sağlayıcısı.

qwen2.5:3b ile mesaj listesinden bir cevap metni üretir. Ollama yerel servis olarak
modeli kendi yönetir (yükleme + GPU) — Foundry'deki singleton/download/load koduna
gerek yok, dosya çok daha sade. Üst katman yine sadece chat(messages) çağırır.
"""

import ollama

from app.config import settings


def chat(messages: list[dict]) -> str:
    """OpenAI formatındaki mesaj listesinden tek bir cevap metni üretir.

    messages örn: [{"role": "system", "content": "..."},
                   {"role": "user", "content": "..."}]
    """
    response = ollama.chat(model=settings.chat_model_alias, messages=messages)
    return response["message"]["content"]
