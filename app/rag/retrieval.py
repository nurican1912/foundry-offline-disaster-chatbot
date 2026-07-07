"""Retrieval Motoru (Modül D) — sorguya anlamca en yakın chunk'ları bulur.

D1: kosinüs benzerliği · D2: top-k retrieval · D3: güvenlik eşiği.
"""

import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """İki vektör arasındaki kosinüs benzerliği. Yüksek = anlamca yakın (~0..1)."""
    # TODO (1): Nokta çarpımı — a ile b'nin elemanlarını eş eş çarpıp topla.
    #   dot = sum(x * y for x, y in zip(a, b))

    # TODO (2): Büyüklükler (norm) — her vektörün kareler toplamının karekökü.
    #   norm_a = math.sqrt(sum(x * x for x in a))
    #   norm_b = math.sqrt(sum(x * x for x in b))

    # TODO (3): dot / (norm_a * norm_b) döndür.
    #   Ama sıfıra bölmeyi engelle: norm_a veya norm_b 0 ise 0.0 döndür.

    raise NotImplementedError
