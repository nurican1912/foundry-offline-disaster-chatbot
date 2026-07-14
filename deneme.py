"""Hızlı deneme aracı — RAG asistanına arka arkaya soru sorabilirsin.
Çalıştır:  python deneme.py
(Modeller ilk soruda yüklenir, sonraki sorular hızlıdır.)
"""

import sys

# Windows konsolu (cp1254) bazı karakterleri basamayıp çökebiliyor; utf-8'e çevir.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from app.rag.pipeline import answer

print("Acil Durum Asistanı — deneme")
role = input("Rol seç [victim / rescuer] (boş = victim): ").strip() or "victim"
print(f"\nRol: {role}. Soru yaz, çıkmak için 'q' yaz.\n")

while True:
    soru = input("Soru: ").strip()
    if soru.lower() in ("q", "quit", "exit", "çık"):
        print("Görüşürüz.")
        break
    if not soru:
        continue
    print("\n" + answer(soru, role) + "\n")
