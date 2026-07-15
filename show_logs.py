"""query_log okuma aracı — sorulan soruları / korpus deliklerini gözden geçir.

Çalıştır:  python show_logs.py

Amaç: hangi sorulara "bilmiyorum" dedik (ve NE KADAR yakındık = top_score)?
Böylece hangi konularda kaynak eklemek gerektiğini görürsün.
"""

import sqlite3
import sys

# Windows konsolu (cp1254) bazı karakterleri basamayıp çökebiliyor; utf-8'e çevir.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from app.config import settings


def show_rejected() -> None:
    """'bilmiyorum' (rejected) denen sorular — skora göre AZALAN (az kalmışlar üstte)."""
    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ts, query, top_score FROM query_log "
        "WHERE outcome = 'rejected' ORDER BY top_score DESC"
    )
    rows = cursor.fetchall()

    print(f"\n=== 'Bilmiyorum' denen sorular ({len(rows)} adet) — skora göre ===\n")
    for row in rows:
        print(f"{row[2]:.2f}  {row[1]}   ({row[0]})")


    conn.close()


if __name__ == "__main__":
    show_rejected()
