"""RAG Pipeline (Modül E3) — soru + rol -> cevap.

Sıfır halüsinasyon garantisi burada kod seviyesinde: retrieval boş dönerse
LLM'e HİÇ gidilmez; doğrulanmış bilgi yok mesajı döner.
"""

from app.ai.chat import chat
from app.rag.prompts import SYSTEM_PROMPTS, NO_CONTEXT_MESSAGE
from app.rag.retrieval import get_relevant_chunks
# NOT: Karar 4 (agent alaka kapısı) MVP'den çıkarıldı — zayıf model gerçek acilleri
# ("başım dönüyor" vb.) reddediyordu (tehlikeli). Kod app/rag/agent.py'de duruyor,
# iyi bir sınıflandırıcı gelince geri bağlanacak. Bkz KARSILASTIGIMIZ_ZORLUKLAR Zorluk 6.


def format_sources(chunks: list[dict]) -> str:
    """Kullanılan chunk'ların kaynaklarını tekilleştirip 'Kaynaklar:' bloğu üretir.

    Deterministik (koddan) — model kaynak uydurmaz. Cevabın SONUNA eklenir.
    """
    sources = []
    for c in chunks:
        if c["source"] not in sources:
            sources.append(c["source"])
    return "\n\nKaynaklar: " + ", ".join(sources)



def answer(query: str, role: str) -> str:
    """Kullanıcının sorusuna, rolüne uygun ve yalnızca korpustan grounded cevap üretir."""

    # 1) İlgili chunk'ları getir (güvenlik eşiği dahil)
    chunks = get_relevant_chunks(query)

    # 2) Güvenlik kapısı: context boşsa LLM'e HİÇ gitme, reddet
    if not chunks:
        return NO_CONTEXT_MESSAGE
        # Karar 5: en iyi eşleşme Q&A ise, doğrulanmış cevabı LLM'siz döndür (hızlı + kusursuz)
    top = chunks[0]
    if top["type"] == "qa":
        # ilk satır=soru, gerisi=cevap
        return top["content"].split("\n", 1)[1].strip() + format_sources([top])

    # 3) Context'i kur: chunk metinlerini aralarına boş satır koyarak birleştir
    context = "\n\n".join(c["content"] for c in chunks)

    # 4) Mesajları kur: system = role promptu + bağlam, user = soru
    system_prompt = SYSTEM_PROMPTS[role] + "\n\nBAĞLAM:\n" + context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    # 5) Modele sor, cevabı döndür
    return chat(messages) + format_sources(chunks)
