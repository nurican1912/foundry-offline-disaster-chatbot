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
- ✅ **Modül D — Retrieval Motoru:** `app/rag/retrieval.py`. `cosine_similarity` (D1), `retrieve` (D2: soruyu embed et → 420 chunk ile karşılaştır → top_k skorlu döndür), `get_embedded_chunks` (DB'den vektörlü chunk'lar), `get_relevant_chunks` (D3: en iyi skor eşik altıysa boş dön → LLM atlanır). **Sıfır halüsinasyon kapısı kod seviyesinde çalışıyor.**
  - **Eşik kalibre edildi:** gerçek veride ilgili sorular 0.63–0.72, alakasız 0.35–0.44 → aralarında net boşluk. `similarity_threshold = 0.5` doğrulandı (config varsayılanı yeterli). Skorların dar banda sıkışması embedding anizotropisinden, veri eksikliğinden değil.
- ✅ **Modül E — LLM Entegrasyonu ve Prompt Mühendisliği:** `app/ai/chat.py` (E1: chat client, embeddings.py deseni), `app/rag/prompts.py` (E2: victim/rescuer system prompt + NO_CONTEXT_MESSAGE), `app/rag/pipeline.py` (E3: `answer(query, role)` — get_relevant_chunks → boşsa reddet → context+prompt kur → chat). **Uçtan uca test geçti:** ilgili soru grounded cevap (halüsinasyon yok), alakasız/kapsam-dışı → "Bu konuda doğrulanmış bir bilgiye sahip değilim". RAG çekirdeği çalışıyor.
  - **Bilinen recall açığı:** "bacağım çok ağrıyor" gibi belirsiz belirti soruları eşiği geçemeyip reddedilebiliyor. Çözüm kolları (ileride): eşiği 0.45'e düşür / korpusu büyüt (queries logu, Madde 2) / retrieval'ı güçlendir (Instruct-Query format + hibrit kelime araması, Madde 3). Kuralı esnetmeden.

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

**Modül F — Backend API (FastAPI).** RAG pipeline (`answer(query, role)`) hazır; şimdi onu bir HTTP endpoint'iyle dışarı açacağız. (F1) FastAPI temelleri + Pydantic request/response modelleri, (F2) `/chat` endpoint (role + mesaj alır, `answer`'ı çağırır, cevap döner), (F2.5) `queries` tablosu + loglama (cevaplanan/cevaplanamayan + top_score), (F4) CORS + hata yönetimi. Frontend (G) bundan sonra bağlanır.

---

## 8. Mimari Kararlar — İleri Faz (2026-07-11)

Foundry Local → **Ollama (GPU)** geçişi sonrası alınan yön kararları. Önkoşul: model önce.

- **Faz 0 — Model (önkoşul):** qwen2.5:3b Türkçesi yetersiz (bozuk, "Afiyet olsun" gibi). Daha güçlü çok-dilli modele geç: **qwen2.5:7b** (VRAM 4 GB'a sıkışık → kısmen CPU offload, biraz yavaş). Aşağıdaki kararların çoğu buna bağlı.
- **Karar 1 — İngilizce birinci sınıf:** İngilizce sorulara Türkçe kadar iyi İngilizce cevap (diğer diller LLM'in gücüne kalır). bge-m3 cross-lingual + prompt'a "kullanıcının dilinde cevapla" + İngilizce kaynak (Karar 3).
- **Karar 2 — Kaynakça gösterme (zorunlu):** Getirilen chunk'ların `source`'undan **deterministik** "Kaynaklar:" bloğu (kod ile, halüsinasyonsuz); opsiyonel inline atıf.
- **Karar 3 — Korpus genişletme (TR+EN):** Çok sayıda otoriter yeni kaynak. İçerik otoriter kaynaklardan (kullanıcı getirir/onaylar); Claude yapılandırma/chunk/ingest/gap-analizi yapar. Re-embed + re-kalibrasyon.
- **Karar 4 — Agent alaka kapısı [MVP DIŞI / ERTELENDİ]:** Fikir: offline LLM sınıflandırıcı her soruya "afet/ilk yardım ile ilgili mi? EVET/HAYIR" der; HAYIR → reddet (telefon-tamiri sızıntısını çözer). **Denendi ve çıkarıldı:** qwen2.5:3b güvenilir sınıflandırıcı değil — "başım dönüyor", "kanama var" gibi gerçek acilleri reddediyordu (tehlikeli yanlış-negatif). Kod `app/rag/agent.py`'de saklı; iyi sınıflandırıcı gelince geri bağlanır. Bkz Zorluk 6.
- **Karar 5 — Pipeline rafinasyonu (Q&A doğrudan / sıkı-grounded LLM):** Q&A eşleşmesinde doğrulanmış cevabın içeriği KORUNUR; LLM onu yeniden yazmaz — sadece kullanıcının durumuna **uyarlar** ve gerekirse **çevirir**, talimatları değiştirmeden/çıkarmadan/eklemeden. Prose'da tightly-grounded sentez. (Sebep: LLM'e mükemmel Q&A cevabını yazdırmak onu bozuyor; ama kullanıcı soruyu farklı ifade ettiği için tam verbatim de yetmez → uyarlama gerek.)
- **Karar 6 — Durum-kilitli prompt:** Victim promptu, kullanıcının ŞU AN afet içinde/mahsur/hastane-doktora ulaşımsız olduğunu **dayatır**; "doktora danış / hastaneye git / ayağa kalk / hareket et" gibi klişeleri **YASAKLAR** (bağlam açıkça söylemedikçe).
- **Karar 8 — Dil-farkında retrieval (iki dilli destek için):** İki dilli korpusta (TR+EN) bge-m3 cross-lingual olduğu için İngilizce soru Türkçe chunk'a da eşleşebilir → Karar 5 yanlış dilde cevap döndürür. Çözüm: her chunk'a `language` (`tr`/`en`) etiketi + sorunun dilini algıla + `retrieve`'de aynı dildeki chunk'ları filtrele (rol filtresi gibi). Böylece İngilizce soru → İngilizce chunk → İngilizce cevap; TR → TR. Karar 1/3 ile birlikte ele alınır. (İngilizce Q&A kaynakları kullanıcı hazırlayacak.)
- **Karar 7 — Triyaj / konuşma modu (MVP DIŞI, sonra eklenecek):** LLM sadece cevaplayan değil, **geri soru soran** bir triyaj asistanı olur. Örn. "bacağımı hissetmiyorum" → "hareket ettirme, şunu yap, ve kontrol et: kanama var mı? ağrı var mı?". Belirsiz belirti sorularında ve retrieval yanlış eşleşmelerinde (Q&A verbatim'in katı kaldığı yerde) çok daha sağlam. **Maliyet:** çok-turlu konuşma (hafıza/state + arayüz → Modül F/G işi) + LLM'i her zaman devreye sokar (yavaşlar) + iyi model ister (4 GB'da zor). Bu yüzden MVP sonrası. Yakın-vadede yanlış eşleşmeler korpus ekleyerek (Karar 3) azaltılır.

**Sıralama (MVP):** Karar 5 (✅) → Karar 6 (✅ durum-kilitli prompt) → Karar 2 (kaynakça) → Karar 1 + Karar 8 (İngilizce + dil-farkında retrieval) → Karar 3 (korpus, süregelen) → Modül F (FastAPI). **MVP dışı:** Karar 4 (agent — zayıf model güvensiz, ertelendi), Karar 7 (triyaj), Karar 8 tam iki dilli destek (F/G'den sonra).

> Not: Faz 0'daki qwen2.5:7b denendi ve **çok yavaştı** (28-38 sn, VRAM offload); qwen3:4b düşünme kapatılamadığı için **220 sn**. 4 GB VRAM'de hem hızlı hem iyi model yok (bkz [[karsilastigimiz-zorluklar]] Zorluk 5). Karar: hızlı küçük model (**qwen2.5:3b**) + **Karar 5** ile kaliteyi mimariden al. Residual model adayı: phi-4-mini.
