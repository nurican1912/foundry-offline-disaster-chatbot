# Afet Asistanı — Victim (Afetzede) | Deprem Dışı Afetler Soru-Cevap Veri Seti

> **Kaynak notu:** Bu dosya RAG vektör veritabanına aktarılmak üzere hazırlanmış tohum veridir ve
> **deprem dışı** afetleri kapsar (sel, yangın, çığ, heyelan, hortum, yıldırım, tsunami, karbonmonoksit,
> kimyasal sızıntı, aşırı sıcak/soğuk, boğulma, izdiham, buzda düşme).
> İçerik genel kabul görmüş afet davranış ve ilk yardım ilkelerine dayanır. **Gerçek bir hayat-güvenliği
> sistemine girmeden önce her madde resmi AFAD, Kızılay ve ilgili kurum (Meteoroloji, İtfaiye, Orman Genel
> Müdürlüğü) kaynaklarıyla çapraz doğrulanmalıdır.** Her maddedeki `Kaynak` alanı, doğrulama yapılacak
> otorite tipini gösterir; canlıya almadan önce ilgili resmi dokümanla eşleştir.
>
> **Mod:** victim
> **Format:** Her başlık + altındaki cevap tek bir chunk. Embedding'i soru ağırlıklı üret (kullanıcı girdisi ≈ soru).

---

## 1. Sel suyu evime doluyor ve yükseliyor, ne yapmalıyım?
**Kategori:** Sel | **Kaynak:** AFAD sel/su baskını rehberi (doğrulanacak)
Yukarı çık — üst kata veya çatıya. Akan suya girme; 15 cm akan su bile seni devirir. Mümkünse elektriği ana panelden kapat ama ıslak elle dokunma. Yanına telefon, düdük ve açık renk bir bez al; çatıda/pencerede kendini belli et. Su altında kalan kapıyı zorlama, akıntı kapıyı açtığında seni içeri çekebilir. Kurtarılmayı bekle, tek başına yüzerek uzaklaşmaya çalışma.

---

## 2. Aracımla sürerken önümde su birikintisi/sel var, geçmeli miyim?
**Kategori:** Sel | **Kaynak:** AFAD sel + karayolu güvenliği (doğrulanacak)
Geçme, geri dön. Derinliği ve altındaki yolun sağlam olup olmadığını göremezsin; yol çökmüş olabilir. 30 cm akan su çoğu aracı yüzdürür, 60 cm ise sürükler. "Dön, boğulma" ilkesini uygula: su üstünden geçmeye çalışmak, sel ölümlerinin en yaygın nedenidir. Alternatif, yüksek bir güzergâh bul.

---

## 3. Aracım sel suyunda mahsur kaldı ve su yükseliyor, ne yapmalıyım?
**Kategori:** Sel / araç | **Kaynak:** AFAD sel + araç güvenliği (doğrulanacak)
Beklemeden hareket et: kemerini çöz, camı aç ya da kır (yan cama sert/sivri cisimle vur, ön cam kırılmaz). Kapılar dış su basıncından açılmayabilir, bu yüzden çıkış yolun cam. Çıkınca aracın çatısına ya da yüksek sağlam bir noktaya geç, akıntının tersine değil çapraz olarak yüksek zemine yönel. Aracın içinde suyun kapıları açacak kadar dolmasını bekleme, o çok geç olabilir.

---

## 4. Ani sel beni yürürken yakaladı ve akıntı sürüklüyor, ne yaparım?
**Kategori:** Sel / boğulma | **Kaynak:** Kızılay boğulma/ilk yardım (doğrulanacak)
Çırpınıp direnme, enerjini tüketir. Ayaklarını akıntı yönünde ve yüzeye yakın tut (baş yukarı, ayak ileri) ki önündeki cisimlere ayağınla çarpasın, kafanla değil. Tutunabileceğin sabit bir cisim (ağaç, direk) gör görmez ona sarıl. Sığ ve yavaş kıyıya doğru çapraz ilerle. Ayağın dibe takılırsa zorlama, akıntı seni suya bastırabilir.

---

## 5. Bulunduğum binada yangın çıktı ve mahsur kaldım, ne yapmalıyım?
**Kategori:** Yangın | **Kaynak:** İtfaiye/AFAD yangın güvenliği (doğrulanacak)
Dumandan uzak, kapısı olan bir odaya çekil ve kapıyı kapat. Kapı altındaki boşluğu ıslak bezle tıka ki duman girmesin. Pencereye git, açıp açık renk bez sallayarak ve seslenerek kendini belli et. Yere yakın dur, temiz hava aşağıdadır. Bir kapıyı açmadan önce elinin sırtıyla sıcaklığını yokla; sıcaksa açma. Yüksekten atlamayı yalnızca alçak kattaysan ve başka hiçbir seçenek yoksa düşün.

---

## 6. Üzerimdeki giysiler tutuştu, ne yapmalıyım?
**Kategori:** Yangın / yanık | **Kaynak:** Kızılay yanık ilk yardımı (doğrulanacak)
Koşma — koşmak alevi büyütür. **Dur, yere yat, yuvarlan.** Yere yatıp elini yüzüne kapat ve alev sönene kadar bir taraftan diğerine yuvarlan. Yakınında battaniye/kalın kumaş varsa alevin üstüne örterek boğ. Alev söndükten sonra yanık bölgeyi 20 dakika serin (buz değil) suyla soğut, yapışan kumaşı çekip çıkarma.

---

## 7. Orman yangını yaklaşıyor ve açık alanda kaçamıyorum, ne yaparım?
**Kategori:** Orman yangını | **Kaynak:** Orman Genel Müdürlüğü/AFAD orman yangını (doğrulanacak)
Yanabilir bitki örtüsünden uzak, açık ve çıplak bir alan (taşlık, sürülmüş tarla, geniş yol, dere yatağı) bul; alev en az yanacak yeri arar. Mümkünse çukur/hendeğe sığın. Pamuklu/yünlü giysiyle vücudunu ve özellikle burun-ağzını kapat; sentetik kumaş erir, kullanma. Ateşin geliş yönünün tersine, yamaç aşağı ve rüzgar tersine kaç (yangın yokuş yukarı ve rüzgarla hızlanır). Suya yakınsan sığ, açık suya gir.

---

## 8. Kapalı bir yerdeyim, baş ağrısı-baş dönmesi-mide bulantısı başladı, karbonmonoksit olabilir mi?
**Kategori:** Karbonmonoksit | **Kaynak:** AFAD/Sağlık Bakanlığı CO zehirlenmesi (doğrulanacak)
Olabilir — soba, şofben, jeneratör veya mangaldan sızan karbonmonoksit renksiz ve kokusuzdur; baş ağrısı, baş dönmesi, bulantı, halsizlik ilk belirtileridir. **Hemen temiz havaya çık**, kapı-pencereleri aç. İçeride oyalanma, bilinç hızla kaybolabilir. Aynı ortamdaki diğer kişileri ve varsa uyuyanları da uyandırıp dışarı al. Dışarı çıkınca 112'yi ara; belirtiler geçse bile değerlendirilmen gerekir.

---

## 9. Çığ beni yakaladı, sürüklenirken ne yapmalıyım?
**Kategori:** Çığ | **Kaynak:** AFAD çığ güvenliği (doğrulanacak)
Ayakta kalmaya ve çığın kenarına doğru "yüzerek" (yüzme hareketleriyle) çıkmaya çalış. Bir ağaç/kayaya tutunabilirsen tutun. Durmadan hemen önce **bir elini yüzünün önüne, bir kolunu yukarı** kaldır: yüzünün önündeki el bir hava boşluğu oluşturur (nefes almak için), yukarıdaki kol yüzeye yakınsan görünmeni sağlar. Kar durunca hangi yön yukarı belli değilse tükür; yer çekimi tükürüğü aşağı götürür, sen ters yöne kaz.

---

## 10. Çığ altında gömülü kaldım, ne yapmalıyım?
**Kategori:** Çığ | **Kaynak:** AFAD çığ güvenliği (doğrulanacak)
Panikle çırpınma; oksijenini ve hava boşluğunu tüketirsin. Ağzının önünde oluşturduğun boşluğu koru, sığ ve yavaş nefes al. Bir elin yüzeye yakınsa hareket ettirmeyi dene ki arama ekibi görsün. Bağırmayı sürekli değil, yakında ses/hareket sezdiğinde yap — kar sesi yutar, enerjini boşa harcama. Sıkışmışsan zorlanma; kurtarma ekipleri çığ bölgesinde hızlı çalışır, dayan.

---

## 11. Heyelan (toprak kayması) belirtileri görüyorum, ne yapmalıyım?
**Kategori:** Heyelan | **Kaynak:** AFAD heyelan rehberi (doğrulanacak)
Uyarı işaretlerini ciddiye al: yeni çatlaklar, eğilen ağaç/direkler, çamurlu suyun aniden artması, kayan zemin sesleri. Kayma hattından **yana doğru** hızla uzaklaş (yukarı-aşağı değil, çünkü kütle yamaçtan iner). Vadi tabanından, dere yatağından ve yamaç eteğinden uzak dur. İçerideysen ve çıkamıyorsan üst kata çık, sağlam bir mobilyanın altına kıvrıl ve başını koru. Gece istirahatte bu belirtileri fark edersen uyanık kal ve tahliyeye hazır ol.

---

## 12. Hortum/kasırga uyarısı var, nerede saklanmalıyım?
**Kategori:** Hortum/kasırga | **Kaynak:** Meteoroloji/AFAD şiddetli hava (doğrulanacak)
En alt katta, **pencerelerden uzak** bir iç oda, koridor veya tuvalet/banyo gibi küçük, dört duvarlı bir alana geç. Yere çök, başını ve enseni ellerinle veya sağlam bir örtüyle koru; mümkünse sağlam bir masanın altına gir. Pencere ve dış duvarlardan uzak dur, camlar patlayabilir. Karavanda/hafif yapıdaysan orayı terk et, sağlam binaya sığın. Açık alandaysan alçak bir çukura yat ve başını koru; araca güvenme.

---

## 13. Açık alandayım ve şimşek/yıldırım var, ne yapmalıyım?
**Kategori:** Yıldırım | **Kaynak:** Meteoroloji/AFAD yıldırım güvenliği (doğrulanacak)
Tek başına yükselen ağaç, direk, tepe noktası gibi yüksek nesnelerden uzaklaş — yıldırım en yükseğe düşer. Su ve metalden (tel çit, bisiklet) uzak dur. Sığınacak sağlam bina/araç yoksa: alçak bir yere git, ayaklarını birleştirip **çömel**, topuklarını kaldır, başını eğ, ellerini kulaklarına koy. Yere **yatma** (toprak üzerinden yayılan akım daha çok yer kaplar). Bir gruptaysan aranıza mesafe koyun. Gök gürültüsünü duyuyorsan zaten menzildesin, hemen sığın.

---

## 14. Sahildeyim, deniz aniden çekildi/tsunami uyarısı var, ne yaparım?
**Kategori:** Tsunami | **Kaynak:** AFAD/Kandilli tsunami uyarısı (doğrulanacak)
Denizin anormal çekilmesi doğal bir tsunami uyarısıdır — resmi uyarıyı bekleme, **hemen yüksek yere ve iç kesime** koş. Mümkün olduğunca yükseğe çık (yüksek kat sağlam binalar da olur) ve sahilden uzaklaş. İlk dalga en büyüğü olmayabilir; dalgalar saatlerce sürebilir, bu yüzden yetkililer güvenli demeden geri dönme. Eşyanı toplamak için vakit harcama, dakikalar hayat kurtarır.

---

## 15. Zehirli gaz/kimyasal bulutu var ve dışarıda mahsurum, ne yapmalıyım?
**Kategori:** Kimyasal sızıntı | **Kaynak:** AFAD KBRN/kimyasal olay (doğrulanacak)
Ağzını-burnunu ıslak bezle kapat ve bulutun **rüzgar üstüne ve yükseğe** doğru, kaynaktan uzaklaş (ağır gazlar alçakta ve çukurda birikir). İçeri girebiliyorsan gir, kapı-pencereleri kapat, havalandırma/klimayı durdur, kapı altlarını ıslak bezle tıka (yerinde sığınma). Yetkililer "tahliye" mi "yerinde kal" mı diyor, resmi anonsa uy. Kimyasal cildine/gözüne bulaştıysa bol suyla yıka ve bulaşan giysiyi çıkar.

---

## 16. Aşırı sıcakta halsizlik, baş dönmesi ve bulantı hissediyorum, ne yapmalıyım?
**Kategori:** Aşırı sıcak | **Kaynak:** Sağlık Bakanlığı/AFAD sıcak hava (doğrulanacak)
Bunlar sıcak bitkinliği belirtisidir, ciddiye al. Hemen serin ve gölge bir yere geç, uzan ve bacaklarını hafif kaldır. Fazla giysini çıkar, cildini ıslat ve yelpazelen. Azar azar su iç. Bilincin bulanıklaşır, terlemez ve derin sıcaklık hissedersen bu daha tehlikeli olan sıcak çarpmasıdır; vücudunu soğutmaya devam ederken acil yardım iste. Sıcak saatlerde tekrar güneşe çıkma.

---

## 17. Kar fırtınası/aşırı soğukta açıkta mahsur kaldım, ne yapmalıyım?
**Kategori:** Aşırı soğuk | **Kaynak:** Meteoroloji/AFAD kış afetleri (doğrulanacak)
Rüzgardan korunacak bir sığınak (araç, duvar dibi, kar siperi) bul ve orada kal; kör edici tipide yürümeye çalışmak kaybolmaya yol açar. Zeminle aranı yalıt (karton, dal, çanta), ısı en çok temas eden yüzeyden kaçar. Üzerine bulduğun her şeyi giy, başını-boynunu kapat, kollarını gövdene çekip kıvrıl. Islanmayı önle. Araçtaysan içinde kal, egzozun karla tıkanmadığından emin ol (CO riski) ve motoru aralıklı çalıştır. Kendini görünür kıl.

---

## 18. Denizde yüzerken güçlü bir akıntı beni açığa çekiyor (rip akıntısı), ne yaparım?
**Kategori:** Boğulma / akıntı | **Kaynak:** Kızılay/sahil güvenlik boğulma (doğrulanacak)
Akıntıya karşı yüzerek savaşma, en güçlü yüzücüyü bile yorup batırır. Akıntı seni kıyıdan uzaklaştırır ama derine batırmaz. **Kıyıya paralel** (sahil boyunca, yana doğru) yüz; akıntı bandı genelde dardır, kısa sürede dışına çıkarsın. Akıntıdan kurtulunca çapraz olarak kıyıya yönel. Yorulursan sırtüstü dönüp sakince yüzerek dinlen ve kolunu kaldırıp yardım işareti ver, panikleme.

---

## 19. Kalabalıkta sıkıştım ve izdiham başladı, ne yapmalıyım?
**Kategori:** İzdiham | **Kaynak:** AFAD/kalabalık güvenliği (doğrulanacak)
Ayakta kalmak en önemli şey — yere düşersen kalkman zorlaşır. Kollarını bir boksör gibi göğsünün önünde kenetle; bu, ciğerlerine nefes alacak boşluk bırakır (izdihamda ölüm genelde ezilmeden değil, göğüs sıkışıp nefes alınamamasındandır). Akıntıya direnme, kalabalığın hareketiyle git ve fırsat buldukça **çapraz olarak kenara** doğru süzül. Yere bir şey düşürürsen alma, eğilme. Duvar/köşeye sıkışmaktan kaçın.

---

## 20. Buzla kaplı göl/deredeyken buz kırıldı ve suya düştüm, ne yaparım?
**Kategori:** Buzda düşme | **Kaynak:** AFAD/Kızılay soğuk su & boğulma (doğrulanacak)
Panik ilk 1 dakikadaki nefes şokunu tetikler; nefesini kontrol etmeye çalış, geçecek. Düştüğün yöne (buzun sağlam olduğu bilinen yön) dön. Kollarını buzun üstüne koy, bacaklarını su yüzeyine paralel getirip yüzer gibi tekmele ve kendini buzun üstüne **kaydırarak** çık, dikey tırmanmaya çalışma. Çıkınca ayağa kalkma; ağırlığını yayarak **yuvarlanarak** kıyıya uzaklaş. Sonra ıslak giysiden kurtulup hemen ısınmaya geç.

---

## 21. Sel/su baskınından sonra su çekildi, eve/evime dönmek güvenli mi?
**Kategori:** Sel sonrası | **Kaynak:** AFAD sel sonrası güvenlik (doğrulanacak)
Hemen dönme, yetkililer güvenli demeden girme. Su binanın temelini, elektrik ve gaz tesisatını bozmuş olabilir. Islak ortamda elektrik düğmelerine dokunma, gaz kokusu varsa girme ve alev/kıvılcım oluşturma. Sel suyu kanalizasyon ve kimyasalla kirlidir; temas ettiğin yerleri yıka, o suyu içme ve bulaşan gıdayı tüketme. Çatlak duvar, oynayan tavan gibi yapısal hasar varsa içeri girme.

---

## 22. Yangın merdiveninde/çıkışta duman çok yoğun, geçmeli miyim yoksa geri mi dönmeliyim?
**Kategori:** Yangın | **Kaynak:** İtfaiye yangın tahliyesi (doğrulanacak)
Yoğun dumanın içine dalma; birkaç nefes bile bilinç kaybına yol açabilir. Geçiş kısaysa ve öte tarafta güvenli çıkış olduğunu biliyorsan, yere yakın sürünerek ve ağzını ıslak bezle kapatarak hızlı geç. Ama duman koyu, sıcak ve nereye çıktığı belirsizse geri dön, kapısı kapatılabilen bir odaya çekil ve pencereden kendini belli et. "Bilinmeyen dumanın içine girmektense güvenli odada beklemek" çoğu zaman daha doğrudur.

---

## 23. Fırtına/sel sırasında elektrik direği devrildi, kablo yerde, ne yapmalıyım?
**Kategori:** Elektrik / fırtına | **Kaynak:** AFAD/enerji dağıtım güvenliği (doğrulanacak)
Yerdeki hiçbir kabloya ve ona değen su birikintisi, çit veya metale **dokunma ve yaklaşma** — kablo canlı olabilir ve zemin üzerinden akım yayılır. En az birkaç metre uzakta kal. O bölgeden uzaklaşman gerekiyorsa, ayaklarını yerden kesmeden **küçük ve bitişik adımlarla** (topuk-parmak, ayakları ayırmadan) uzaklaş; büyük adım atmak bacakların arasında gerilim farkı oluşturup çarpılmaya yol açabilir. Durumu yetkililere bildir.

---

## 24. Bulunduğum bölge için tahliye emri verildi, ne yapmalıyım?
**Kategori:** Tahliye | **Kaynak:** AFAD tahliye talimatları (doğrulanacak)
Emri ciddiye al ve geciktirme; "bir şey olmaz" diye beklemek tahliye ölümlerinin başlıca nedenidir. Önceden hazırladıysan acil çantanı (su, ilaç, kimlik, telefon-şarj, el feneri, biraz para) al. Yetkililerin gösterdiği güzergâh ve toplanma alanını kullan, kestirme/kapalı yollara sapma. Gaz ve elektriği kapat, kapıları kilitle. Yakınlarına nereye gittiğini bildir. Aracı olanlar depoyu önceden doldursun; trafik kilitlenirse aracı bırakıp yaya devam etmek gerekebilir.

---

## 25. Bir afetten sağ kurtuldum ama sürekli tetikte, uyuyamıyor ve o anı yeniden yaşıyorum
**Kategori:** Psikolojik / travma | **Kaynak:** Sağlık Bakanlığı/AFAD psikososyal destek (doğrulanacak)
Yaşadığın karşısında bu tepkiler (uykusuzluk, irkilme, o anı tekrar tekrar görme, suçluluk, uyuşukluk) normaldir ve bir zayıflık değildir — beynin ağır bir olayı işliyor. İlk günlerde temel ihtiyaçlarına (uyku, su, yemek, güvenli ortam) ve güvendiğin insanlarla bağ kurmaya odaklan. Kafein ve alkolden uzak dur, bunlar belirtileri artırır. Şikayetler haftalarca sürer, yoğunlaşır ya da günlük hayatını engellerse bir ruh sağlığı uzmanından destek al; afet sonrası psikososyal destek hatları tam bunun için vardır.

---
