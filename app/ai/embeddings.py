"""AI Layer — Ollama tabanlı embedding sağlayıcısı.

Metinleri bge-m3 ile 1024-boyutlu vektöre çevirir. Ollama yerel bir servis olarak
modeli kendi yönetir (yükleme + GPU) — bu yüzden Foundry'deki singleton/download/load
koduna artık gerek yok, dosya çok daha sade.

Üst katman (ingestion, retrieval) yine sadece embed_text/embed_texts/embed_query
çağırır; altındaki sağlayıcının Ollama olduğunu bilmez.
"""

import ollama

from app.config import settings


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Bir metin listesini vektör listesine çevirir (toplu)."""
    response = ollama.embed(model=settings.embedding_model_alias, input=texts)
    return response["embeddings"]


def embed_text(text: str) -> list[float]:
    """Tek bir metni tek bir vektöre çevirir."""
    return embed_texts([text])[0]


def embed_query(text: str) -> list[float]:
    """Sorguyu vektöre çevirir. bge-m3'te sorgu/doküman aynı biçimde embed edilir
    (qwen3'teki 'Instruct:' önekine gerek yok), o yüzden embed_text ile aynı."""
    return embed_text(text)
