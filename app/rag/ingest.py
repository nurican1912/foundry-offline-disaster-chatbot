"""Ingestion köprüsü (B3 parça 3) — chunk'ları embed edip veritabanına yazar.

database.py (oku/yaz) ile embeddings.py (metin -> vektör) parçalarını birleştirir.
İki katman birbirini bilmez; bu dosya ikisini import edip aralarında köprü kurar.
"""

from app.ai.embeddings import embed_text
from app.data.database import get_chunks_without_embedding, save_embedding


def embed_pending_chunks(db_path: str) -> int:
    """Vektörü olmayan tüm chunk'ları embed edip veritabanına kaydeder.

    İşlenen (embed edilen) chunk sayısını döndürür.
    """
    chunks = get_chunks_without_embedding(db_path)
    if not chunks:
        print("İşlenecek yeni chunk bulunamadı. Her şey güncel.")
        return 0
    
    print(f"Toplam {len(chunks)} adet chunk vektöre çevrilecek. Bu işlem bilgisayarın hızına göre biraz sürebilir...")

    # Her chunk için: metni vektöre çevir, sonra o vektörü satırına kaydet.
    for i, chunk in enumerate(chunks, start=1):
        vector = embed_text(chunk["content"])          # metin -> vektör (embeddings.py)
        save_embedding(db_path, chunk["id"], vector)   # vektörü o id'li satıra yaz (database.py)

        if i % 50 == 0:                                 # her 50'de bir ilerleme
            print(f"  {i}/{len(chunks)} tamamlandı")

    print(f"Bitti: {len(chunks)} chunk embed edildi.")
    return len(chunks)