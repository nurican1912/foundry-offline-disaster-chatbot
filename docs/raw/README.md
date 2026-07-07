# Kaynak Dökümanlar — `docs/raw/`

Bu klasör, asistanın **tek bilgi kaynağıdır**. Sistem yalnızca buradaki içerikten
konuşur (sıfır halüsinasyon ilkesi). Buraya konan her şey doğrulanmış olmalı.

## Kurallar

1. **Yalnızca resmi/doğrulanmış kaynaklar.** AFAD, Kızılay, Sağlık Bakanlığı ilk
   yardım rehberleri vb. Blog, forum, "duyduğuma göre" → YASAK.
2. **Format:** `.md` veya `.txt`, **UTF-8**. Düz akan metin; karmaşık tablo/görsel
   değil. (PDF okuma ileride Modül H1'de; şimdilik metni elle temizleyip koy.)
3. **Dosya adı = kaynak etiketi.** Açıklayıcı, kebab-case. Örn:
   `afad-deprem-aninda.md`, `ilkyardim-kanama-kontrolu.md`,
   `kurtarici-triyaj-temel.md`. Bu ad, veritabanında her parçanın `source`
   alanı olarak kullanılacak (atıf için).
4. **Provenans (önerilir):** Dosyanın ilk satırına kaynağın künyesini yaz
   (örn. `> Kaynak: AFAD Afet Bilinci Kılavuzu, 2023`).

## Kapsama hedefi (dual-mode)

Dökümanlar her iki rolü de beslemeli:

- 🔴 **Victim (afetzede):** enkaz altında davranış, enerji/efor koruma, panik
  azaltma, ses/işaret verme.
- 🟢 **Rescuer (kurtarıcı):** temel triyaj, güvenli müdahale adımları, ikincil
  riskler (gaz sızıntısı, boyun/omurga kırığı şüphesi, kanama kontrolü).

## MVP kapsamı

5–8 odaklı doküman yeterli. Önce çalışan sistem, sonra zenginleştirme.
