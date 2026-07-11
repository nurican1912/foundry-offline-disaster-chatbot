# Karşılaştığımız Zorluklar

Bu dosya, proje boyunca karşılaştığımız sorunları ve çözümlerini kaydeder.
Her giriş: **Sorun → Teşhis → Çözüm → Durum** biçiminde.

---

## Zorluk 1 — Gerçek kullanıcı soruları haksız yere "bilmiyorum" ile reddediliyor

**Sorun:**
Sistemi gerçek kullanıcı gibi, günlük dille test ettik. Meşru acil durum soruları
reddedildi:
- "bacağım galiba kırıldı" → "Bu konuda doğrulanmış bir bilgiye sahip değilim."
- "bacağımı hissetmiyorum" → aynı ret.
- "bacağımın üzerine taş düştü" → aynı ret.

Oysa korpusta bu konular (kırık, ezilme, his kaybı) **var**.

**Teşhis:**
`retrieve()` ile ham skorlara baktık. Doğru chunk **bulunuyordu** ama skoru
güvenlik eşiğinin (0.5) hemen altındaydı:
- "bacağım galiba kırıldı" → **0.456** → doğru chunk: "Kemiğimin kırıldığını
  düşünüyorum, ne yapmalıyım?" — ama 0.456 < 0.5 olduğu için reddedildi.
- "kanama var" → 0.476, "başım dönüyor" → 0.473 → hepsi doğru chunk, hepsi eşik altı.

Sebepler:
1. Eşik 0.5, korpusa **benzer biçimde** yazılmış test sorularıyla kalibre edilmişti.
   Gerçek **günlük** ifadeler daha düşük skor alıyor.
2. qwen3-embedding'in Türkçe skorları dar banda sıkışık (anizotropi). İlgili (0.43–0.48)
   ile alakasız (kek 0.443) bandı **çakışıyordu** → eşiği düşürmek tek başına temiz çözmüyor.

**Çözüm:**
qwen3-embedding, **sorgu** tarafında bir "instruction" (yönerge) bekliyor. Sadece
kullanıcı sorusunu `"Instruct: ...\nQuery: " + soru` önekiyle embed ettik; dokümanlar
öneksiz kaldı, korpus yeniden işlenmedi. Etki (ölçüldü):
- bacağım galiba kırıldı: 0.456 → **0.583**
- bacağımı hissetmiyorum: 0.43 → **0.535**
- kanama var: 0.476 → **0.674**
- kek (alakasız): 0.443 → 0.45 (aynı), tatil: 0.425 → 0.397 (aşağı)

İlgili sorular yukarı fırladı, alakasızlar aynı/aşağı → ayrım açıldı.
Kod: `app/ai/embeddings.py`'ye `embed_query()` + `QUERY_INSTRUCTION`; `app/rag/retrieval.py`
sorguyu artık `embed_query` ile embed ediyor.

**Durum: KISMEN ÇÖZÜLDÜ — İKİ AÇIK MADDE VAR:**
1. **Eşik yeniden kalibre edilmeli.** Kodda kullanılan gerçek (Türkçe karakterli)
   yönergeyle "kek tarifi" tekrar 0.5'i geçip cevaplanabildi. Alakasızlar sızmasın,
   ilgililer geçsin diye eşik gerçek yönergeyle yeniden ölçülecek.
2. **Model kalitesi (daha ciddi, ayrı zorluk).** qwen2.5-1.5b, doğru context'i alsa
   bile cevabı bozuk/tehlikeli üretiyor. Örn. "bacağım kırıldı" → "kendi kendine hareket
   etmeye çalışın" (YANLIŞ — kırıkta hareket zarar verir). Muhtemel çözüm:
   `chat_model_alias`'ı daha büyük modele çevirmek. Bkz Zorluk 2/3.

---

## Zorluk 2 — GPU'yu devreye alma denemesi (kısmen başarısız)

**Sorun:** Cevap kalitesi için daha büyük model gerekiyor ama CPU'da büyük model yavaş.
Kullanıcının NVIDIA RTX 3050 Ti (4 GB VRAM) GPU'su var; GPU kullanabilir miyiz?

**Teşhis:**
- Başta `foundry service status` "GPU (WinML) Windows 11 build 26100 ister" demişti; ben
  bunu "GPU hiç kullanılamaz" diye fazla geniş yorumladım. Yanlıştı.
- `discover_eps()` → `CUDAExecutionProvider` mevcut (kayıtsız). CUDA, WinML'den ayrı bir yol.
- `download_and_register_eps(['CUDAExecutionProvider'])` → **başarıyla kaydedildi** (~3 dk).
- AMA: kayıttan sonra (katalog zorla yenilendi bile) SDK kataloğundaki **46 modelin hepsi
  CPU** (`deviceType=CPU`, `CPUExecutionProvider`). **Tek bir GPU/CUDA model varyantı yok.**
  CLI `foundry model list`'teki "generic-gpu" varyantları SDK'nın bu makineye sunduğu
  filtrelenmiş katalogda görünmüyor.

**Sonuç:** CUDA kaydedildi ama **çalıştıracak GPU modeli yok** → GPU chat için kullanılamıyor.
Modeller CPU'da koşacak.

**Yan kazanımlar (boşa gitmedi):**
- Model cache C:'den **D:\foundry_models**'e taşındı (C: doluydu). `config.py`'ye
  `model_cache_dir` eklendi, `.env`'de `MODEL_CACHE_DIR=D:\foundry_models`.
- Eski chat modelleri (qwen2.5-0.5b, 1.5b) silindi (~2.6 GB açıldı).

**Durum: KAPANDI (GPU yok).** Devam: qwen3-4b'yi CPU'da test et (Zorluk 1'in model maddesi).

---

## Zorluk 3 — CPU tıkanıklığı ve Foundry Local dışına (GPU'lu offline modele) geçme

**Sorun:**
Foundry GPU sunmadığı için (Zorluk 2) her şey CPU'da. qwen3-4b CPU testi:
- Yavaş: enkaz 21.7 sn, kek 57.8 sn — afet asistanı için kabul edilemez.
- qwen3 bir "düşünen" (reasoning) model; `<think>` bloğu üretiyor → daha da yavaş.
  `/no_think` ile kapatıldı ama hız yine yetersiz.
- Cevap kalitesi zayıf ("enkaz altında" → sadece "Sakin ol").
- **Güvenlik hatası:** instruct formatı skorları topluca yükseltince "kek tarifi" 0.5'i
  geçti ve modele kek tarifi UYDURTTU → sıfır halüsinasyon deliği. Eşik kalibrasyonu şart.
CPU'da daha büyük model = daha yavaş; yani kaliteyi büyük modelle çözmek CPU'da kapalı.

**Öneri (kullanıcı):** Foundry Local'i bırakıp embedding + chat modellerini, GPU'da
(CUDA / RTX 3050 Ti, 4 GB VRAM) **offline** çalışan modellere geçirmek.

**Fizibilite:** NVIDIA GPU + CUDA çalışıyor. Ollama gibi bir araç GGUF modelleri GPU'da
offline koşturur, hem chat hem embedding sunar. 4 GB VRAM'e Q4 quantize 3-4B chat +
küçük embedder (bge-m3 / e5 — Türkçesi daha iyi) sığar ve hızlıdır.

**Mimari etki:** AI katmanı izole → sadece `app/ai/embeddings.py` + `app/ai/chat.py`
değişir; retrieval/pipeline/db/chunking aynı. AMA embedding modeli değişince korpus
YENİDEN embed edilmeli + eşik yeniden kalibre edilmeli (veri işi).

**Bedel:** Ollama kurulumu, model indirmeleri, re-embed, kalibrasyon.

**Kritik karar:** Bu, projeyi "Microsoft Foundry Local" çerçevesinden çıkarır. Foundry
zorunlu değilse mühendislik olarak sağlam; zorunluysa proje kimliğini değiştirir.

**Durum: KARARLAŞTIRILIYOR (kullanıcı onayı bekleniyor).**
