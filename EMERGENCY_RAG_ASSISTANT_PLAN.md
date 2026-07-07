# Offline Acil Durum Asistanı — Proje Planı ve Çalışma Kuralları

> Bu dosya, projeyi AI ile birlikte adım adım inşa ederken referans alınacak context dosyasıdır.
> Yeni bir oturuma başlarken (özellikle Claude Code gibi farklı bir araçta) bu dosya baştan okunmalı —
> hem proje mimarisini hem de çalışma kurallarını içeriyor.

---

## 0. Kaynak Analizi ve Teknoloji Yığını Kararı

İki kaynak incelendi: `Summer_School_Foundry_Local_Plan.docx` ve azurefeeds.com / Microsoft Tech Community'deki Foundry Local RAG yazısı. **Karar: Python + FastAPI.**

- Internship programı tarafında bir teknoloji dayatması olmadığı doğrulandı — seçim tamamen bizim.
- docx'in haftalık ders akışı (Week 1–4) baştan sona Microsoft Learn'ün Python tutorial'ını temel alıyor (`foundry-local-sdk`, `main.py`, Python `sqlite3`). Python + FastAPI bu akışla birebir örtüşüyor.
- Azurefeeds/Tech Community'deki Node.js/Express örneği değerlendirildi ama bilinçli olarak kullanılmadı — sebebi "yanlış" olması değil, **PharmaBot projesinde FastAPI zaten zorunlu olarak kullanılacak olması.** Bu projeyi FastAPI ile yapmak, takım projesine düşük riskli bir ortamda pratik yapmış olarak girmek anlamına geliyor.
- Node.js/Express pratiği bilinçli olarak ayrı bir projeye ertelendi — bu projede karışıklık yaratmaması için tek dil/tek framework (Python) ile gidiliyor.
- Aynı anda alınan LangChain/RAG kursundaki LangServe bölümü (FastAPI üzerine kurulu) artık alakasız bir tangent değil, doğrudan bu projeye uygulanabilir bir konu.
- docx'teki model isimleri (`phi-1.5-mini`, `qwen3-embedding-0.6b` vb.) tutarsız/şüpheli. **Gerçek model adları `foundry model list` ile doğrulanacak.**

---

## 1. Proje Vizyonu

İnternet altyapısının tamamen çöktüğü büyük afet durumlarında (deprem vb.) hayat kurtarmak amacıyla tasarlanmış, tamamen yerel cihazda çalışan bir **RAG tabanlı Acil Durum Asistanı**.

**Temel ilke — Sıfır Halüsinasyon:** Sistem yalnızca vektör veritabanına aktarılmış, doğrulanmış resmi afet/ilk yardım rehberlerinden beslenir. Tıbbi tavsiye uydurmak veya varsayım yapmak kesinlikle yasak. Benzerlik skoru düşükse LLM devre dışı bırakılır, sistem direkt "Bu konuda doğrulanmış bir bilgiye sahip değilim." der.

**Roller:**
- **Sen (mimar):** Genel sistem tasarımı, prompt mühendisliği, mimari kararlar.
- **Claude (rehber):** Kodu sen yazıyorsun, ben açıklıyorum/kontrol ediyorum/hata ayıklıyorum — aşağıdaki kurallara göre.

---

## 2. Çalışma Kuralları (Her Oturumda Geçerli)

**Kural 1 — Parçalama:** Proje, profesyonel bir senior mühendisin yapacağı gibi parçalanır. Birden fazla teknoloji varsa önce teknoloji teknoloji ayrılır, sonra her teknoloji kendi içinde anlamlı alt parçalara bölünür.

**Kural 2 — Önce anlat, sonra bekle:** Yazılacak her anlamlı kod parçası için önce mantık detaylı anlatılır (neden bu yapı, hangi kavram, nasıl çalışıyor), kod **verilmez** — yazman için beklenir. Görev net bir "Görevin: ..." cümlesiyle kapanır.

**Kural 3 — Hata analizi:** Yazdığın kod analiz edilir, hatalar varsa hangi kavram karışıklığından kaynaklandığı açıklanır (sadece "yanlış" denmez, *neden* yanlış olduğu gösterilir), sonra çalışan doğru kod verilir.

**Kural 4 — Bilgi eksikliği direktifi:** Bir konuyu/aracı anlamadığını söylediğinde, genel bir açıklama yerine net bir öğrenme direktifi verilir (örn. "FastAPI'nin dependency injection sistemini öğren, anladığında devam ederiz" / "Şu şu başlıkları çalış, bekliyorum").

---

## 3. Mevcut Bilgi Seviyesi (Eldeki Malzeme)

| Teknoloji | Seviye |
|---|---|
| Python | Sağlam temel — **ana implementasyon dili** |
| FastAPI | Yeni — PharmaBot'ta da zorunlu kullanılacak, burada önden pratik yapılıyor |
| SQL | Biliyor, **SQLite hiç kullanmamış** (Python `sqlite3` modülüyle) |
| RAG (kavram) | Mantığı biliyor, **hiç proje yapmamış** |
| HTML/CSS/JS (frontend) | Yapabilir |
| React | Detaylı anlatılırsa yapabilir — MVP'de basit kalınacak, ileri fazda opsiyon (dil seçimi önemsiz, JS zaten biliniyor) |
| Node.js / Express | Bilinçli olarak bu projeye dahil edilmedi — ayrı bir projede odaklı şekilde öğrenilecek |
| Foundry Local SDK (Python) | Yeni — `pip install foundry-local-sdk` üzerinden öğrenilecek |

---

## 4. Mimari Genel Bakış

Beş katman, tamamen tek makinede:

1. **Client (Frontend):** Basit HTML/CSS/JS — iki büyük buton, mesaj alanı. Afet anında kullanıcı uzun yazamaz, telefon kullanır → mobil öncelikli, minimal UI.
2. **Server (FastAPI):** `/chat` endpoint'i — rol parametresi (`victim` / `rescuer`) + kullanıcı mesajını alır, RAG pipeline'ını tetikler.
3. **RAG Pipeline:** Sorguyu embed eder, kosinüs benzerliğiyle top-k chunk getirir, güvenlik eşiğini kontrol eder (eşik altıysa LLM'e gitmeden ret).
4. **Data Layer (SQLite):** Chunk'lar + embedding'ler + kaynak metadata + upsert için içerik hash'i.
5. **AI Layer (Foundry Local):** Embedding modeli + chat modeli, Python SDK üzerinden, tamamen cihaz üzerinde.

### Dual-Mode Mantığı

- 🔴 **Victim Mode:** "Sen enkaz altındaki birine yardım eden bir asistansın. Talimatlarını çok kısa, net ve panik azaltıcı şekilde ver. Efor ve enerji tasarrufunu vurgula. Sadece veritabanından sana verilen bağlamı kullan."
- 🟢 **Rescuer Mode:** "Sen bir ilk yardım ve operasyon asistanısın. Kurtarıcıya adım adım, güvenli müdahale ve triyaj talimatları ver. İkincil riskleri (gaz sızıntısı, boyun kırığı şüphesi vb.) mutlaka hatırlat. Sadece veritabanından sana verilen bağlamı kullan."

Buton seçimi → `role` parametresi → backend'e iletilir → ilgili system prompt seçilir.

### Güvenlik Bariyeri (Kritik)

Benzerlik skoru eşik altındaysa LLM çağrılmaz. Bu, prompt'a gömülen bir "kibarca reddet" talimatı değil, **kod seviyesinde zorunlu bir kapı** — eşik kontrolü retrieval fonksiyonunun kendisinde yapılacak.

---

## 5. Modül Bazlı Yol Haritası

Kural 1'e göre önce teknoloji, sonra o teknoloji içinde anlamlı parçalar.

### Modül A — Ortam ve Foundry Local Temelleri (Python)
- A1. Foundry Local kurulumu + doğrulama (`foundry model list`, basit model çalıştırma)
- A2. Python SDK ile "Hello Model" testi — tek seferlik chat completion çağrısı
- A3. Proje iskeleti: klasör yapısı, `requirements.txt`, config/env yönetimi

### Modül B — Veri Toplama ve Hazırlama
- B1. Kaynak doküman seçimi ve organizasyonu (AFAD kılavuzları, ilk yardım rehberleri, deprem davranış talimatları → `docs/raw/`)
- B2. Chunking stratejisi: dökümanları anlamlı parçalara bölme fonksiyonu
- B3. Embedding üretimi: her chunk için Foundry Local embedding modeliyle vektörleştirme

### Modül C — SQLite Veri Katmanı
- C1. Şema tasarımı: `chunks` tablosu (id, source, content, embedding, content_hash)
- C2. Upsert mantığı: aynı içerik tekrar geldiğinde güncelleme/atlama (hash bazlı dedup)
- C3. Sorgu fonksiyonları: tüm embedding'leri çekme, kaynağa göre filtreleme

### Modül D — Retrieval Motoru
- D1. Kosinüs benzerliği fonksiyonu
- D2. Top-k retrieval (3–4 chunk)
- D3. Güvenlik eşiği: skor eşik altıysa context boş döner → üst katman LLM'i atlar

### Modül E — LLM Entegrasyonu ve Prompt Mühendisliği
- E1. Foundry Local chat client kurulumu
- E2. Rol bazlı system prompt şablonlarının koda bağlanması (Victim/Rescuer — promptların kendisi mimar tarafından tasarlandı, burada implementasyonu yapılıyor)
- E3. Bağlam + soru birleştirme, LLM çağrısı, "context yoksa cevap üretme" davranışının kodda garanti altına alınması

### Modül F — Backend API (FastAPI)
- F1. FastAPI temelleri: route tanımlama, Pydantic request/response modelleri
- F2. `/chat` endpoint: `role` + mesaj alır, pipeline'ı çağırır, cevap döner
- F3. `/ingest` endpoint (opsiyonel, ileri faz): yeni doküman ekleme tetikleyici
- F4. CORS, temel hata yönetimi

### Modül G — Frontend (HTML/CSS/JS)
- G1. Statik sayfa: iki büyük buton + mesaj input + cevap alanı
- G2. `fetch` ile FastAPI'ye istek, rol state yönetimi
- G3. Mobil uyumlu, yükleniyor durumu net gösterilen basit UX
- G4. *(İleri faz, opsiyonel)* React'e geçiş

### Modül H — Dinamik Ingestion ve Ölçeklenebilirlik (İleri Faz)
- H1. PDF/TXT/MD okuma + chunking pipeline'ının modülerleştirilmesi
- H2. Yeni dosya eklendiğinde otomatik tetiklenen ingestion akışı
- H3. Upsert mantığının genişletilmesi (temel C2'de atıldı)

### Modül I — Test, Güvenlik Doğrulama, Sunum
- I1. Halüsinasyon testleri: veritabanında olmayan sorularla ret davranışının doğrulanması
- I2. Cevaplanabilir soru seti ile doğruluk testi
- I3. README ve sunum hazırlığı

---

## 6. Sıralama Mantığı

Foundry Local + Python temeli her şeyin önkoşulu → veri olmadan retrieval olmaz → SQLite, retrieval mantığından önce hazır olmalı → retrieval, LLM entegrasyonundan önce çalışır halde olmalı (LLM'e besleyecek context lazım) → LLM pipeline'ı bitmeden API yazmanın anlamı yok → API hazır olmadan frontend'in bağlanacağı bir yer yok → dinamik ingestion ve React, MVP çalıştıktan sonraki zenginleştirmeler. Test, her modülün sonunda mini şekilde yapılır; Modül I sadece toplu/sistemli doğrulama içindir.

---

## 7. Şu An Durum

**Teknoloji yığını kararı kesinleşti (Python + FastAPI) — buradan sonra değişmeyecek.**

### Tamamlanan modüller

- ✅ **Modül A — Ortam ve Foundry Local Temelleri**
  - A1: Foundry Local kuruldu (CLI 0.8.119) ve doğrulandı.
  - A2: Python SDK köprüsü çalışıyor (`foundry-local-sdk` **1.2.3** — import `foundry_local_sdk`; `Configuration` + `FoundryLocalManager.initialize` + `catalog.get_model` + `get_chat_client` API'si). "Hello Model" testi geçti.
  - A3: Proje iskeleti kuruldu (`app/` katmanlı paketler, `.venv`, `requirements.txt`, `.gitignore`, `pydantic-settings` tabanlı `app/config.py`).
- ✅ **Modül B1 — Kaynak Doküman Seçimi:** `docs/raw/` içinde 8 doğrulanmış `.md` — ~160 Q&A (victim/rescuer × deprem/deprem-dışı) + Sağlık Bakanlığı İlk Yardım rehberi ve afet dökümanları. PDF orijinaller `veriler/`'de arşivde.
- ✅ **Modül B2 — Chunking:** `app/rag/chunking.py`. Yapı-farkında (başlık-tabanlı) bölme. Her chunk ortak sözlük yapısına normalize edilir: `{content, source, type (qa/prose), role (victim/rescuer/None), category}`.
  - `chunk_qa_markdown` / `chunk_prose_markdown` (alt kat: tek metni böler) → `load_qa_chunks` / `load_prose_chunks` (orta kat: dosyaları otomatik gezer) → `get_all_chunks` (üst kat: tek giriş noktası, ingestion bunu çağıracak).
  - Sonuç: **420 chunk** (150 Q&A + 270 prose), 8 kaynak. Başlıksız dosya (`Deprem-Öncesi-...md`) `## ` başlıkları eklenerek normalize edildi.
  - Bilinen ufak borç: 20 prose chunk 1000+ karakter (uzun-bölüm ikincil bölme, gerekirse ileride); PDF→md kaynaklı ufak artıklar (`- Ø` madde işaretleri vb.).
- ✅ **Modül C (C1+C2+C3 okuma/yazma) — SQLite Veri Katmanı:** `app/data/database.py`. `chunks` tablosu (id, source, content, type, role, category, content_hash UNIQUE, embedding TEXT/JSON). `init_db` (şema), `save_chunks` (hash'li idempotent upsert — `ON CONFLICT DO NOTHING`), `get_chunks_without_embedding` + `save_embedding` (okuma/güncelleme). Tüm SQL parametreli (`?`). 420 chunk kalıcı.
- ✅ **Modül B3 — Embedding Üretimi:** `app/ai/embeddings.py` (embed_text/embed_texts, model bir kez yüklenir) + `app/rag/ingest.py` (`embed_pending_chunks`: oku→embed→yaz köprüsü). **420 chunk'ın hepsi 1024-boyutlu vektöre çevrilip DB'ye yazıldı.** Bilgi tabanı aranabilir durumda.

### Alınan önemli kararlar / kısıtlar

- **Chat modeli (aday):** `qwen2.5-1.5b` — CPU'da tutarlı Türkçe (0.5b kelime salatası verdi). Nihai seçim Modül E'de.
- **Donanım:** Windows 10 build 19045, GPU/NPU hızlandırma yok (WinML build 26100 istiyor) → CPU-only, küçük model.
- **Embedding: ÇÖZÜLDÜ (2026-07-02).** Bloke değil. Tüm "embedding yok" sorunu CLI'nin (`foundry model list`) gösterme hatasıymış (7 ERR CLI-tarafı). Model kataloğda baştan beri vardı; **SDK üzerinden erişiliyor**.
  - Model: `qwen3-embedding-0.6b` (id `qwen3-embedding-0.6b-generic-cpu:1`), task=embeddings, CPU, ONNX, 495 MB, **1024 boyutlu** vektör. İndirildi, çalışıyor.
  - Erişim: `mgr.catalog.get_model("qwen3-embedding-0.6b")` → `download/load` → `get_embedding_client().generate_embedding(text)` / `generate_embeddings(list)`.
  - **Kalite uyarısı:** Türkçe skorlar dar banda sıkışık (parafraz ~0.57, alakasız ~0.37 — sıralama doğru, ayrım zayıf). B3'te qwen3-embedding'in "Instruct:/Query:" sorgu formatını test et (skorları açabilir). `similarity_threshold` 0.5 OLMAYACAK — gerçek veriyle (`queries.top_score` logu) kalibre edilecek.
  - Model değişirse tüm korpus yeniden embed edilmeli + eşik yeniden kalibre edilmeli.
  - **Sonuç: B3 ve D1 artık ilerleyebilir. Proje tıkanıklıktan çıktı.**

### Sıradaki adım

**Modül D — Retrieval Motoru.** Bilgi tabanı hazır (420 vektörlü chunk). Şimdi: (D1) kosinüs benzerliği fonksiyonu, (D2) top-k retrieval, (D3) güvenlik eşiği (skor eşik altıysa boş dön → LLM atlanır). Kalibrasyon notu: `similarity_threshold` gerçek skorlara göre ayarlanacak; qwen3-embedding query-instruction formatı test edilecek.
