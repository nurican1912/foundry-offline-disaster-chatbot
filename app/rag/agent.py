"""Agent alaka kapısı (Karar 4) — offline LLM sınıflandırıcı.  [MVP DIŞI / ERTELENDİ]

Her soru için (eşik aşılsın aşılmasın) "bu soru afet/acil/ilk yardım alanıyla ilgili mi?"
diye karar verir. İlgisizse pipeline soruyu reddeder — "telefon tamiri" gibi eşik
sızıntılarını kapatmayı amaçlar.

!!! ŞU AN PIPELINE'A BAĞLI DEĞİL. Sebep: qwen2.5:3b (4 GB VRAM'e sığan zayıf model) bir
sınıflandırıcı olarak güvenilmez — Türkçe günlük belirtileri ("başım dönüyor", ilk halde
"kanama var") "afet değil" sanıp GERÇEK ACİLLERİ reddediyordu (tehlikeli yanlış-negatif).
Güvenlik matematiği: yanlış-pozitif (telefon sızar) tehlikesiz; yanlış-negatif (acili
reddet) tehlikeli. O yüzden MVP'den çıkarıldı. Kod burada duruyor; iyi bir sınıflandırıcı
(daha büyük/daha iyi model, ya da farklı yaklaşım) gelince pipeline.answer() başına geri
bağlanır. Bkz KARSILASTIGIMIZ_ZORLUKLAR.md Zorluk 6.
"""

from app.ai.chat import chat

# Talimat İngilizce (instruction-following güçlü). Modelden SADECE YES/NO isteniyor.
RELEVANCE_PROMPT = (
    "You are a safety classifier for a disaster and first-aid assistant. "
    "The user may describe an injury, illness, pain, or dangerous situation in casual, "
    "everyday language (in Turkish or English). "
    "If the message could POSSIBLY relate to health, injury, pain, bleeding, breathing, "
    "safety, an emergency, a disaster, or first aid — answer YES. "
    "Answer NO ONLY if the message is clearly about a completely unrelated topic such as "
    "cooking/recipes, entertainment, sports, travel, shopping, or repairing devices. "
    "When in doubt, answer YES. "
    "Answer with ONLY one word: YES or NO."
)


def is_disaster_related(query: str) -> bool:
    """Soru afet/acil/ilk yardım alanıyla ilgili mi? True/False döner."""
    messages = [
        {"role": "system", "content": RELEVANCE_PROMPT},
        {"role": "user", "content": query},
    ]
    cevap = chat(messages)
    return "YES" in cevap.upper()
