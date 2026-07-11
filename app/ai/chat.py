"""AI Layer — Foundry Local chat (sohbet) sağlayıcısı.

Chat modelini (qwen2.5-1.5b) bir kez yükler ve OpenAI formatındaki mesaj
listesinden bir cevap metni üretir. embeddings.py ile AYNI desen
(singleton + modül düzeyi önbellek), sadece embedding yerine sohbet.
"""

from foundry_local_sdk import Configuration, FoundryLocalManager

from app.config import settings

_chat_client = None


def _get_client():
    """Chat client'ı (gerekirse indirip yükleyerek) tek sefer hazırlar."""
    global _chat_client
    if _chat_client is not None:
        return _chat_client

    # 1. Manager singleton'ını hazırla (embeddings.py'deki gibi):
    if FoundryLocalManager.instance is None:
        FoundryLocalManager.initialize(Configuration(
            app_name=settings.app_name,
            model_cache_dir=settings.model_cache_dir or None,
        ))
    
    manager = FoundryLocalManager.instance

    # 2. CHAT modelini al, cache'te değilse indir, yükle:
    model = manager.catalog.get_model(settings.chat_model_alias)
    if not model.is_cached:
        model.download(lambda p: None)
    model.load()

    # 3. Client nesnesini oluştur ve döndür:
    _chat_client = model.get_chat_client()
    
    return _chat_client


def chat(messages: list[dict]) -> str:
    """OpenAI formatındaki mesaj listesinden tek bir cevap metni üretir.

    messages örn: [{"role": "system", "content": "..."},
                   {"role": "user", "content": "..."}]
    """
    # 4. İstemciyi çağır ve gelen mesajları tamamlayıp çıktıyı döndür
    client = _get_client()
    completion = client.complete_chat(messages)
    
    return completion.choices[0].message.content