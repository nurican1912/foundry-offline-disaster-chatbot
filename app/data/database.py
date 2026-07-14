"""Data Layer — SQLite bağlantısı ve şema.

chunks tablosu, get_all_chunks'ın ürettiği parçaları kalıcı saklar.
embedding sütunu şimdilik NULL kalır; embedding çözülünce (B3) doldurulur.
"""

import hashlib
import json
import sqlite3


def init_db(db_path: str) -> None:
    """Veritabanını (yoksa) oluşturur ve 'chunks' tablosunu kurar."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    content TEXT,
    type TEXT,
    role TEXT,
    category TEXT,
    content_hash TEXT UNIQUE,
    embedding TEXT
    );""")
    conn.commit()   # değişiklikleri kaydet
    conn.close()


def save_chunks(db_path: str, chunks: list[dict]) -> int:
    """Chunk listesini veritabanına yazar. content_hash ile dedup (upsert).

    Aynı içerik (aynı hash) zaten varsa atlanır. embedding şimdilik NULL kalır
    (B3'te doldurulacak). Yeni eklenen satır sayısını döndürür.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    inserted = 0

    for chunk in chunks:
        # 1) İçeriğin parmak izi (aynı içerik -> aynı hash)
        content_hash = hashlib.sha256(chunk["content"].encode("utf-8")).hexdigest()

        # 2) Ekle; ama aynı parmak izi varsa hiçbir şey yapma (dedup)
        cursor.execute(
            "INSERT INTO chunks (source, content, type, role, category, content_hash) "
            "VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(content_hash) DO NOTHING",
            (chunk["source"], chunk["content"], chunk["type"],
             chunk["role"], chunk["category"], content_hash),
        )

        # 3) Gerçekten eklendiyse (1) say, atlandıysa (0) sayma
        inserted += cursor.rowcount

    conn.commit()
    conn.close()
    return inserted


def get_chunks_without_embedding(db_path: str) -> list[dict]:
    """Embedding'i henüz NULL olan chunk'ları döndürür (id + content)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1: embedding'i NULL olan satırların id ve content'ini SELECT et.
    cursor.execute("SELECT id, content FROM chunks WHERE embedding IS NULL")
    rows = cursor.fetchall()   # Örnek çıktı: [(1, "metin1"), (2, "metin2")]

    # 2: Her satırı {"id": ..., "content": ...} sözlüğüne çevirip listeye koy.
    result: list[dict] = []
    for row in rows:
        result.append({
            "id": row[0],
            "content": row[1]
        })

    conn.close()
    return result


def save_embedding(db_path: str, chunk_id: int, vector: list[float]) -> None:
    """Bir chunk'ın embedding'ini JSON metin olarak günceller."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 3: Vektörü (listeyi) JSON metne çevir ve o id'li satırın embedding'ini güncelle.
    cursor.execute(
        "UPDATE chunks SET embedding = ? WHERE id = ?",
        (json.dumps(vector), chunk_id)
    )

    conn.commit()
    conn.close()


def get_embedded_chunks(db_path: str) -> list[dict]:
    """Embedding'i DOLU olan tüm chunk'ları döndürür (retrieval için).

    embedding, DB'de JSON metin olarak duruyor; burada json.loads ile
    tekrar sayı listesine çevrilir.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, content, source, role, type, embedding "
                   "FROM chunks WHERE embedding IS NOT NULL")

    rows = cursor.fetchall()
   
    result: list[dict] = []

    for row in rows:
        # row[4] string tipinde saklanan köşeli parantezli vektör metnidir (ör: "[0.1, 0.5, -0.2]").
        # json.loads() bu metni okuyarak gerçek bir Python listesine çevirir.
        embedding_list = json.loads(row[5])
        
        # Her bir satır verisiyle istenen anahtarlara sahip bir sözlük (dictionary) oluşturuyoruz.
        chunk_dict = {
            "id": row[0],
            "content": row[1],
            "source": row[2],
            "role": row[3],
            "type": row[4],
            "embedding": embedding_list
        }
        
        # Oluşturulan sözlüğü result isimli boş listemize ekliyoruz.
        result.append(chunk_dict)


    conn.close()
    return result

    # TODO (2): Her satır için embedding metnini json.loads ile listeye çevir ve
    #   {"id","content","source","role","embedding"} sözlüğü yapıp result'a ekle.
    #   (row[0]=id, row[1]=content, row[2]=source, row[3]=role, row[4]=embedding metni)