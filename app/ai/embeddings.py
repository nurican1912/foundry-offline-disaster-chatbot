"""AI Layer — Foundry Local embedding sağlayıcısı.

Modeli (qwen3-embedding-0.6b) bir kez yükler ve metinleri 1024-boyutlu vektöre çevirir.
Üst katman (ingestion, retrieval) sadece embed_texts/embed_text çağırır; altındaki
Foundry ayrıntısını bilmez. Sağlayıcı değişirse yalnızca bu dosya değişir.
"""


from foundry_local_sdk import Configuration, FoundryLocalManager
from app.config import settings

# Modeli her çağrıda yeniden yüklemek pahalı. Bir kez yükleyip modül düzeyinde saklarız.
_embedding_client = None


def _get_client():
    """Embedding client'ı (gerekirse indirip yükleyerek) tek sefer hazırlar."""
    global _embedding_client
    if _embedding_client is not None:
        return _embedding_client

    # 1. FoundryLocalManager singleton'ını hazırla.
    if FoundryLocalManager.instance is None:
        FoundryLocalManager.initialize(Configuration(
            app_name=settings.app_name,
            model_cache_dir=settings.model_cache_dir or None,
        ))
    
    manager = FoundryLocalManager.instance

    # 2. Modeli al, cache'te değilse indir, yükle:
    model = manager.catalog.get_model(settings.embedding_model_alias)
    if not model.is_cached:
        # İndirme işlemi için basit bir callback (ilerleme çubuğu vs. istemediğimiz için boş geçiyoruz)
        model.download(lambda p: None) 
    model.load()

    # 3. _embedding_client'ı doldur ve döndür:
    _embedding_client = model.get_embedding_client()
    return _embedding_client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Bir metin listesini vektör listesine çevirir (toplu)."""
    client = _get_client()
    response = client.generate_embeddings(texts)
    # Gelen karmaşık API yanıtının içinden sadece vektör (embedding) kısımlarını çekiyoruz
    return [item.embedding for item in response.data]


def embed_text(text: str) -> list[float]:
    """Tek bir metni tek bir vektöre çevirir. (Dokümanlar/chunk'lar için.)"""
    # Tek elemanlı bir liste olarak toplu fonksiyona yollayıp, dönen listenin ilk (ve tek) elemanını alıyoruz
    return embed_texts([text])[0]


# qwen3-embedding, SORGU tarafında bir yönerge (instruction) bekler. Bu, sorgu
# vektörünü dokümanlara daha iyi hizalar ve ilgili eşleşmelerin skorunu yükseltir.
# Dokümanlar yönergesiz (embed_text) embed edilir; SADECE sorgular embed_query kullanır.
QUERY_INSTRUCTION = (
    "Instruct: Verilen soru için en ilgili ilk yardım ve afet talimatını getir.\nQuery: "
)


def embed_query(text: str) -> list[float]:
    """Kullanıcı sorusunu (yönerge önekiyle) vektöre çevirir. Retrieval bunu kullanır."""
    return embed_text(QUERY_INSTRUCTION + text)