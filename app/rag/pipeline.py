"""RAG Pipeline (Modül E3) — soru + rol -> cevap.

Sıfır halüsinasyon garantisi burada kod seviyesinde: retrieval boş dönerse
LLM'e HİÇ gidilmez; doğrulanmış bilgi yok mesajı döner.
"""

from app.ai.chat import chat
from app.rag.prompts import SYSTEM_PROMPTS, NO_CONTEXT_MESSAGE
from app.rag.retrieval import get_relevant_chunks


def answer(query: str, role: str) -> str:
    """Kullanıcının sorusuna, rolüne uygun ve yalnızca korpustan grounded cevap üretir."""

    # 1) İlgili chunk'ları getir (güvenlik eşiği dahil)
    chunks = get_relevant_chunks(query)

    # 2) Güvenlik kapısı: context boşsa LLM'e HİÇ gitme, reddet
    if not chunks:
        return NO_CONTEXT_MESSAGE

    # 3) Context'i kur: chunk metinlerini aralarına boş satır koyarak birleştir
    context = "\n\n".join(c["content"] for c in chunks)

    # 4) Mesajları kur: system = role promptu + bağlam, user = soru
    # "/no_think": qwen3 düşünme (reasoning) modunu kapatır — CPU'da hız için ve
    # kullanıcıya <think> bloğu sızmasın diye. (Diğer modeller bunu yok sayar.)
    system_prompt = "/no_think\n" + SYSTEM_PROMPTS[role] + "\n\nBAĞLAM:\n" + context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    # 5) Modele sor, cevabı döndür
    return chat(messages)
