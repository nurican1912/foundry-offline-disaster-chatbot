"""Retrieval Motoru (Modül D) — sorguya anlamca en yakın chunk'ları bulur.

D1: kosinüs benzerliği · D2: top-k retrieval · D3: güvenlik eşiği.
"""

import math

from app.ai.embeddings import embed_query
from app.config import settings
from app.data.database import get_embedded_chunks


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """İki vektör arasındaki kosinüs benzerliği. Yüksek = anlamca yakın (~0..1)."""
    
    dot = sum(x*y for x,y in zip(a,b))
    
    norm_a = math.sqrt((sum(x * x for x in a)))
    norm_b = math.sqrt((sum(x * x for x in b)))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
        
    return dot / (norm_a * norm_b)


def retrieve(query: str, db_path: str | None = None, top_k: int | None = None) -> list[dict]:
    """Sorguya anlamca en yakın top_k chunk'ı skorlarıyla döndürür.

    Dönen her öğe: chunk sözlüğü + "score" alanı; skora göre azalan sıralı.
    """
    db_path = db_path or settings.db_path
    top_k = top_k or settings.top_k

    query_vec = embed_query(query)   # yönerge önekli sorgu — ilgili eşleşmeleri güçlendirir

    chunks = get_embedded_chunks(db_path)
    scored = []
    for chunk in chunks:
        score = cosine_similarity(query_vec, chunk["embedding"])
        scored.append((score, chunk))

    scored.sort(key=lambda pair: pair[0], reverse=True)    

    results = []
    for score, chunk in scored[:top_k]:
        new_chunk = {**chunk, "score": score}
        results.append(new_chunk)
    return results


def get_relevant_chunks(
    query: str,
    db_path: str | None = None,
    top_k: int | None = None,
    threshold: float | None = None,
) -> list[dict]:
    """Top-k retrieval + güvenlik eşiği (sıfır halüsinasyon kapısı).

    En iyi (ilk) sonucun skoru eşiğin ALTINDAysa BOŞ liste döner — üst katman
    bunu görüp LLM'i çağırmadan "bilmiyorum" der.
    """
    if threshold is None:
        threshold = settings.similarity_threshold

    results = retrieve(query, db_path, top_k)

    # En iyi sonuç bile eşiğin altındaysa: güvenlik kapısı devreye girer, boş dön.
    if not results or results[0]["score"] < threshold:
        return []

    return results