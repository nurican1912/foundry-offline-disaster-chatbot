"""RAG Pipeline (Modül E3) — soru + rol -> yapılandırılmış sonuç paketi.

Sıfır halüsinasyon garantisi burada kod seviyesinde: en iyi eşleşme eşiğin
altındaysa LLM'e HİÇ gidilmez; "bilmiyorum" paketi döner.

answer() artık düz metin değil, ETİKETLİ bir paket döndürür:
    {"answer": str, "sources": list[str], "outcome": str, "top_score": float}
outcome: 'rejected' (bilmiyorum) | 'qa' (doğrulanmış) | 'prose' (LLM).
Loglama ve JSON'a çevirme PIPELINE'DA DEĞİL, kenarda (API) yapılır — çekirdek saf kalır.
"""

from app.ai.chat import chat
from app.config import settings
from app.rag.prompts import SYSTEM_PROMPTS, NO_CONTEXT_MESSAGE
from app.rag.retrieval import retrieve
# NOT: Karar 4 (agent alaka kapısı) MVP'den çıkarıldı — zayıf model gerçek acilleri
# ("başım dönüyor" vb.) reddediyordu (tehlikeli). Kod app/rag/agent.py'de duruyor,
# iyi bir sınıflandırıcı gelince geri bağlanacak. Bkz KARSILASTIGIMIZ_ZORLUKLAR Zorluk 6.


def unique_sources(chunks: list[dict]) -> list[str]:
    """Chunk'ların kaynaklarını tekilleştirip LİSTE olarak döndürür.

    (Eski format_sources string döndürüyordu; artık kaynaklar pakette ayrı bir
    liste alanı olduğu için düz liste veriyoruz — metne yapıştırmayı tüketiciye bırakıyoruz.)
    """
    sources = []
    for c in chunks:
        if c["source"] not in sources:
            sources.append(c["source"])
    return sources


def answer(query: str, role: str) -> dict:
    """Soruya grounded cevap üretir ve yapılandırılmış paket döndürür (saf: DB'ye yazmaz)."""

    # 1) Skorlu chunk'ları getir. DİKKAT: get_relevant_chunks DEĞİL, retrieve.
    #    retrieve KAPISIZ ve her chunk'a "score" ekliyor → reddetsek bile skoru kaybetmeyiz.
    results = retrieve(query)
    top_score = results[0]["score"] if results else 0.0

    # 2) Güvenlik kapısı (eşiği artık BURADA uyguluyoruz, skor elimizde kalsın diye).
    
    if not results or top_score < settings.similarity_threshold:
        return {"answer": NO_CONTEXT_MESSAGE, "sources": [], "outcome": "rejected", "top_score": top_score}
    

    top = results[0]

    # 3) Karar 5: en iyi eşleşme Q&A ise doğrulanmış cevabı LLM'siz döndür.
    if top["type"] == "qa":
        cevap = top["content"].split("\n", 1)[1].strip()   # ilk satır=soru, gerisi=cevap
        return {"answer": cevap, "sources": unique_sources([top]), "outcome": "qa", "top_score": top_score}

    # 4) Prose yolu: bağlamı kur, role promptuyla LLM'e sor.
    context = "\n\n".join(c["content"] for c in results)
    system_prompt = SYSTEM_PROMPTS[role] + "\n\nBAĞLAM:\n" + context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    cevap = chat(messages)
    return {"answer": cevap, "sources": unique_sources(results), "outcome": "prose", "top_score": top_score}
