# Yerel ve çok dilli kaynak bulma: başlangıç literatür taraması

**Tarih:** 12 Kasım 2026  
**Durum:** Yöntem seçimine hazırlık; nihai yöntem, algoritma, model ve kütüphane kararı açık.  
**Dayanak:** Kullanıcının araştırma amacı ve [proje tanımı](../PROJE_TANIMI.md). Sunumdaki yöntem örnekleri karar veya kısıt olarak kullanılmadı.

[Açıklamalı kaynakça](KAYNAKLAR.md) 26 akademik çalışma ve 6 teknik/uygulamalı kaynağı toplar. [İlk hafta kaydı](ILK_HAFTA.md) tamamlanan araştırma çıktılarıyla sonraki işleri ayırır.

## 1. Literatürün işaret ettiği araştırma konumu

Bu problem; kişisel bilgi erişimi, diller arası bilgi erişimi, ilgililik sıralaması ve verimli indeksleme alanlarının kesişimindedir. Kalıcı yerel indeksleme, kişisel belgeleri yeniden bulmak için uzun süredir kullanılmaktadır. Modern örneklerde yerel indeksin embedding aramasıyla birleştirilmesi de vardır. Dolayısıyla “yerelde indeks oluşturmak” veya “anlamsal arama eklemek” tek başına özgünlük iddiası olmamalıdır. [Stuff I’ve Seen](https://www.microsoft.com/en-us/research/publication/stuff-ive-seen-a-system-for-personal-information-retrieval-and-re-use/), [Recoll anlamsal arama](https://www.recoll.org/pages/recoll-semantic.html).

**Bu taramadan çıkan yorum:** Araştırılabilir katkı; Türkçe–İngilizce kişisel notlarda doğru dosyayı bulma kalitesi, sorgu/güncelleme maliyeti, kısıtlı çıktı ve eşleşme yokluğu davranışının birlikte değerlendirilmesidir. Bu bir “literatürde hiç yapılmadı” iddiası değildir. Bu özel birleşimin ne ölçüde yeni olduğunu söylemek için daha kapsamlı atıf zinciri ve benzer sistem karşılaştırması gerekir.

Mevcut kapsamda sistem nihai cevap üretmez. RAG literatürü, aramanın bir yapay zekâ iş akışına nasıl katkıda bulunabileceğini açıklar; üretim kalitesi sonuçları bizim dosya erişim başarımızın yerine geçmez. [Lewis ve ark.](https://arxiv.org/abs/2005.11401), [çok dilli RAG](https://aclanthology.org/2024.knowllm-1.15/).

## 2. Hipotezi sınanabilir parçalara ayırma

Aşağıdaki maddeler ölçülmesi önerilen alt hipotezlerdir; kanıtlanmış sonuç veya yöntem kararı değildir.

| Alt hipotez | Gerekli karşılaştırma | İddiayı zayıflatacak sonuç |
| --- | --- | --- |
| H1: Kalıcı indeks tekrar eden sorgularda kaynak okumasını azaltır. | Aynı sıralama kuralının her sorguda metin okuyan ve önceden indekslenmiş sürümleri; indeks kurma/güncelleme ayrıca. | Kurma ve güncelleme dahil hedef kullanımda maliyet karşılanmıyorsa veya indeks verisi maliyeti kazancı siliyorsa. |
| H2: Dil/anlam ilişkisini işleyen bir yöntem ifade değişiminde ve TR↔EN erişimde yararlıdır. | Aynı koleksiyon ve sorgularda sözcüksel, çeviri tabanlı ve çok dilli temsil aileleri. | Kazanç yalnızca ortak özel ad içeren örneklerdeyse veya bir dil yönünde ciddi kayıp varsa. |
| H3: Az içerikle yeterli kaynak seçimi yapılabilir. | Aynı çıktı bütçesinde Recall/nDCG; benzer kalitede çıktı baytı ve çağıran aracın okuma davranışı. | Kısa çıktı ilgili dosyaları kaçırıyor veya sonraki okumaları artırıyorsa. |
| H4: İlgili kaynak bulunmayan sorgular ayırt edilebilir. | Ayrılmış doğrulama/test verisinde yanlış kabul ve yanlış ret. | İlgisiz sorguları reddetmek için cevaplanabilir sorguların büyük kısmı kaybediliyorsa. |

“Bütün belgeleri modele vermeye göre daha az çıktı” tek başına yeterli karşılaştırma değildir: kaliteyi de korumak gerekir. Ayrıca sıradan indeksli sözcüksel arama karşılaştırmaya alınmadan bütün kazancı NLP’ye bağlamak hatalı olur. BEIR, basit referansların güçlü olabileceğini gösterir. [BEIR](https://arxiv.org/abs/2104.08663).

## 3. Kararların birbirinden ayrılması

**Temsil**, metnin nasıl kodlandığıdır; **ilgililik modeli**, sorgu–kaynak ilişkisinin nasıl puanlandığıdır; **indeks**, adayların nasıl bulunduğu ve saklandığıdır. **Sonuç politikası** ise kaç dosya döndürüleceğini, açıklamayı ve gerektiğinde sonuç vermemeyi belirler. Bunlar tek bir “algoritma seçimi” altında birbirine karıştırılmamalıdır.

Örneğin aynı embedding modeliyle tam vektör taraması veya yaklaşık komşu araması kullanılabilir. Daha hızlı komşu bulmak, modelin anlamı daha iyi temsil ettiğini göstermez. [Faiss](https://arxiv.org/abs/2401.08281), [HNSW](https://arxiv.org/abs/1603.09320).

| Yaklaşım ailesi | Araştırılacak katkı | Başlıca sınır / maliyet | Kaynak |
| --- | --- | --- | --- |
| TF–IDF / BM25 ve dilsel normalizasyon | Terim, dosya adı, teknik isim, hata kodu gibi kesin ipuçları; az model maliyeti. | Eş anlam, dolaylı ifade ve diller arası uyuşmazlık. Kök bulma özel isimleri bozabilir. | K02, U05, U06 |
| Sorgu/belge çevirisi + sözcüksel erişim | Ortak temsil uzayı yerine metinleri aynı dile getirerek erişim. | Çeviri hatası ve teknik terim kaybı. Sorgu çevirisi çevrimiçi gecikme; belge çevirisi ön işleme/depolama getirir. | K14’te özgün/çevrilmiş koleksiyon düzeni |
| Çok dilli tek vektörlü temsil | Farklı ifadeler ve diller arasında ortak anlam yakınlığı. | Benzer konu ile gerçek ilgililik karışabilir; uzun dosyada bilgi seyrelmesi olabilir. | K04–K07, K21 |
| Öğrenilmiş seyrek temsil | Öğrenilmiş terim ağırlığı/genişletmesi ile ters indeksin birleşimi. | Dil uyumu ve eğitim verisi; genişletilen terimin kaynakta bulunmaması. | K20, K06 |
| Geç etkileşim / çok vektör | Sorgu ve belge içindeki daha ayrıntılı eşleşmeleri koruma. | Daha fazla temsil ve arama işi; çok dilli model gereksinimi. | K19, K06, K25 |
| Sıra birleştirme / hibrit | Farklı sistemlerin tamamlayıcı hatalarından yararlanma. | Bir yöntemin iyi sıralaması diğerinden zarar görebilir; aday havuzu ve ağırlık etkisi. | K03, K11 |
| İkinci aşama yeniden sıralama | Dar aday kümesinde sorgu–belge etkileşimini daha ayrıntılı değerlendirme. | Ek gecikme; ilk aşamada kaçan belge geri gelmez. | K07, U04 |

Çeviri seçeneği için buradaki maliyet ayrımı mühendislik çıkarımıdır; bu projede ölçülmedi. Bütün ailelerin ilk hafta uygulanması önerilmiyor. Önce hangi soruna hangi ailenin cevap verdiğini belirlemek, sonra uygulanabilir adayları seçmek gerekir.

Türkçede yoğun ve geç etkileşimli modelleri doğrudan karşılaştıran TurkColBERT çalışması, aday aileleri geniş tutmayı destekler; çalışmanın çevrilmiş ve orta ölçekli veri sınırları korunmalıdır. RAGTurk ise Türkçe bir hatta daha çok bileşen eklemenin her zaman daha iyi sonuç vermediğini raporlar. Bu bulgular belirli bir modeli seçtirmez, karşılaştırılacak soruları güçlendirir. [TurkColBERT](https://arxiv.org/abs/2511.16528), [RAGTurk](https://arxiv.org/abs/2602.03652).

Hazır model kullanımı, alana uyarlama ve sıfırdan model eğitimi de ayrı kararlardır. Uyarlama ancak eldeki veride sistematik bir eksik görülür ve yeterli etiket/veri sağlanırsa gerekçelendirilebilir. Hazır modelin başarısını ölçmeden özel eğitim zorunlu kabul edilmemelidir.

## 4. Çok dillilik ile diller arası erişim

Dört yön ayrı raporlanmalıdır: **TR→TR, EN→EN, TR→EN, EN→TR**. Karışık dilli dosyalar ayrıca işaretlenmelidir. İlk işaret sorgu, ikinci işaret hedef kaynağın dilidir.

MIRACL ve Mr. TyDi birden fazla dil içerir; temel görevlerinde sorguyla kaynak aynı dildedir. Üstelik bu iki veri kümesinde Türkçe bulunmaz. Dolayısıyla ne doğrudan Türkçe dil içi test ne de Türkçe–İngilizce diller arası test kümesi olarak kullanılabilirler. NeuCLIRBench gerçek diller arası görev düzeni sağlar ancak Türkçe içermez. [MIRACL](https://aclanthology.org/2023.tacl-1.63/), [Mr. TyDi](https://aclanthology.org/2021.mrl-1.12/), [NeuCLIRBench](https://arxiv.org/abs/2511.14758).

LaBSE gibi çeviri çifti bulmada başarılı modeller, aynı cümlenin diğer dildeki karşılığını bulmayı öğretir. “Bu proje neden veritabanını değiştirdi?” sorusuyla uzun bir karar notunu eşleştirmek farklı bir görevdir. [LaBSE](https://aclanthology.org/2022.acl-long.62/).

Türkçe dil içi değerlendirme için **TR-MTEB (2025)** ve **TR-TEB (2026)** daha doğrudan kaynaklardır. İsimleri benzer olsa da ayrı çalışmalardır. Özgün/çevrilmiş veri ayrımı, erişim alt görevleri ve eğitim verisi örtüşmesi incelenmelidir; bunlar da kişisel TR↔EN testinin yerini otomatik olarak almaz. [TR-MTEB](https://aclanthology.org/2025.findings-emnlp.471/), [TR-TEB](https://lrec.elra.info/lrec2026-main-862).

Önerilen veri yaklaşımı: Gerçek veya hassas bilgilerden arındırılmış notlar üzerinde doğal bilgi ihtiyaçları yazılmalı; aynı niyetin çevirileri ve paraphrase’leri aynı veri bölümünde tutulmalıdır. Hem bir dildeki tek kaynağı zorunlu kılan sorgular hem de iki dilde birden ilgili belge bulunabilen sorgular olmalıdır. Aksi halde sistem sürekli İngilizce sonucu seçerek başarılı görünebilir. Bunlar bu proje için deney tasarımı önerileridir.

## 5. Parça, dosya ve açıklama

Dosya sonucu üretmek, dosyanın tek temsilini kullanmayı zorunlu kılmaz. Tam dosya, başlık/bölüm, sabit uzunluklu parça ve örtüşen parçalar karşılaştırılabilir. Parça uzunluğu modelin tokenizer’ı ile kontrol edilmeli; sessiz kırpma uzun dosyanın sonundaki kanıtı yok edebilir.

Parça puanlarını dosya puanına dönüştürmek için maksimum, en iyi birkaç parçanın bileşimi veya öğrenilmiş toplama adaydır. PARADE, bilgi ihtiyacının tek parçada mı yoksa dosya boyunca mı karşılandığının seçimi etkileyebildiğini gösterir. Bu nedenle otomatik olarak “maksimum en iyidir” veya “öğrenilmiş toplama gerekir” sonucu çıkarılamaz. [PARADE](https://eprints.gla.ac.uk/298257/).

Projenin açıklama gereksinimi için **kaynakta bulunan kısa metin + dosya/bölüm konumu** değerlendirilebilir. Bu, kullanıcıya kanıt gösterir; modelin iç kararının nedensel açıklaması olduğu iddia edilmemelidir. Birebir eşleşme ile anlamsal olarak getirilen ifade ayrı etiketlenmelidir. SPLADE benzeri bir modelin genişlettiği sözcük kaynakta yoksa alıntı yapılamaz. [SPLADE](https://arxiv.org/abs/2107.05720).

## 6. Kalıcılık, güncelleme ve bağımsızlık

Aşağıdakiler algoritma seçimine değil, proje gereksinimlerinin karşılanmasına ilişkin tasarım sorularıdır:

- Kaynak kimliği, göreli yol, içerik özeti/hash, parça konumu ve indeks/model sürümü nasıl tutulacak?
- Ekleme, değiştirme, silme ve yeniden adlandırma hangi işlemlerle yansıtılacak? Güncelleme yarıda kesilirse eski ve yeni kayıtlar nasıl ayrılacak?
- Model veya parçalama kuralı değişince hangi indeksler yeniden üretilecek?
- İndeks, deney çıktıları ve aracın kendi dosyaları kaynak havuzundan nasıl dışlanacak?
- Model dosyaları temin edildikten sonra indeksleme ve sorgu ağ kapalıyken çalışabilecek mi? Çıktı herhangi bir yapay zekâ ürünü gerektirmeden okunabilecek mi?

Bunlar henüz uygulanmış davranışlar değildir. SQLite FTS5 ve Faiss gibi bileşenler farklı parçaları sağlar; tek başlarına tüm kaynak yaşam döngüsünü çözmezler. [FTS5](https://www.sqlite.org/fts5.html), [Faiss](https://arxiv.org/abs/2401.08281).

## 7. Kalite–maliyet ölçümü

Birincil sonuç birimi **benzersiz dosya** olmalıdır. Aynı dosyanın beş parçasını ilk beş sonuçta görmek, beş ilgili dosya bulmak olarak sayılmaz.

| Boyut | Aday ölçüm | Dikkat edilecek ayrım |
| --- | --- | --- |
| Sıralama | Recall@k, nDCG@k, MRR@k | Recall: ilgili dosyaların kapsanması; nDCG: dereceli ilgililik/sıra; MRR: ilk ilgili dosya. |
| Dil | Dört dil yönünde ayrı skor ve örnek sayısı | Tek ortalama zayıf yönü gizleyebilir. |
| Sonuç vermeme | Cevapsız sorgularda yanlış kabul; cevaplı sorgularda yanlış ret | Cevapsız sorguda standart Recall paydası sıfırdır; ayrı ölçülmeli. |
| Sorgu | Gecikme dağılımı, kaynak okuma baytı, indeks/model yükleme, çıktı baytı | Sıcak/soğuk çalıştırma ve işletim sistemi önbelleği ayrılmalı. |
| Yaşam döngüsü | İlk indeks süresi, değişiklik güncelleme süresi, disk ve tepe RAM | Sadece sıcak sorgu hızını göstermek yeterli değildir. |
| Çıktının yararı | Aynı bayt/token bütçesinde erişim kalitesi | Token sayısı kullanılıyorsa tokenizer belirtilmeli. |
| İşlevsel doğruluk | Silinen yolun çıkmaması, değişen parçanın yenilenmesi, tekrar sırası | Sıralama puanı ile doğruluk/güncellik birbirinden ayrıdır. |

Sorgu maliyeti farkını NLP ile indekslemeye ayrı ayrı atfetmek için iki deney gerekir: (1) sıralama sabitken kalıcılığı değiştirmek, (2) kalıcı indeks koşulu sabitken erişim yöntemini değiştirmek. Böylece “yeniden dosya okumama” kazancı bir modelin anlamsal başarısı gibi raporlanmaz.

Toplam süre için bir başlangıç hesabı:

`T_indeksli = T_kurma + toplam(T_güncelleme) + Q × ortalama(T_sorgu)`

`T_tarama = Q × ortalama(T_her_sorguda_tarama)`

Bu basitleştirme aynı sorgu/kalite ve aynı güncelleme yükünde yapılmalıdır. Süre, bayt, RAM ve token ayrı birimlerdir; tek maliyet sayısında gelişigüzel toplanmamalıdır. “Kaynak dosyalar okunmadı” da “disk/indeks/model verisi okunmadı” anlamına gelmez.

Lost in the Middle seçici bağlamın motivasyonunu sağlar; uzun bağlam karşılaştırmaları ise bazı koşullarda daha fazla bağlamın kalite yararı sağlayabildiğini gösterir. Bu ikisi birlikte okunmalıdır. Mevcut kapsamda ölçülen küçük arama çıktısı, çağıran yapay zekânın sonraki okumaları da ölçülmeden toplam token tasarrufu diye sunulamaz. [Liu ve ark.](https://aclanthology.org/2024.tacl-1.9/), [Li ve ark.](https://aclanthology.org/2024.emnlp-industry.66/).

## 8. Sonuç vermeme kararı

En yüksek benzerlik, ilgili belge varlığını garanti etmez. Sabit bir cosine veya RRF eşiği bütün modeller ve diller için hazır doğruluk eşiği olarak alınmamalıdır. Aday eşik/politika, ayrı doğrulama kümesinde; hem ilgili hem ilgisiz sorgularla ayarlanmalı ve testte değiştirilmemelidir.

Başlangıçta mutlak puan, ilk iki sonucun farkı veya ayrı ilgililik değerlendiricisi araştırılabilir. Bunlar **aday fikirlerdir**. Özellikle iki gerçekten ilgili dosyanın birbirine yakın puan alması, küçük puan farkını tek başına ret gerekçesi yapmayı riskli kılar. Bu tarama, sonuç vermeme veya anlamsal açıklama için doğrulanmış bir nihai yöntem ortaya koymamıştır; derinleştirilecek başlıklardır.

## 9. Yöntem seçimine geçişte kullanılabilecek karar tablosu

Aşağıdaki tablo doldurulmadan bir kazanan ilan edilmemelidir. Ölçümler henüz yoktur.

| Karar | Açık seçenekler | Seçimi destekleyecek kanıt |
| --- | --- | --- |
| Erişim ailesi | Sözcüksel, çeviri, yoğun, öğrenilmiş seyrek, geç etkileşim, birleşim | Dil yönleri ve sorgu türlerine göre kalite/maliyet. |
| Model | E5, BGE-M3, Qwen3 ve araştırmayla bulunacak diğer uygun adaylar | Aynı değerlendirme kümesinde sonuç, yerel RAM/gecikme, lisans ve çalıştırma koşulları. |
| Temsil birimi | Dosya, bölüm, parça | Uzunluk gruplarında kaçırılan kaynaklar ve açıklama konumunun doğruluğu. |
| İndeks | Ters indeks, tam vektör arama, yaklaşık vektör arama | Koleksiyon büyüklüğüne göre süre, disk, komşu recall’ı ve güncelleme kolaylığı. |
| İkinci aşama | Yok, yeniden sıralama, farklı toplama | Ek maliyet karşılığında ölçülen kalite artışı. |
| Sonuç politikası | Sabit k, eşikli sonuç, bütçeli seçim | Yanlış kabul/ret ve aynı bütçede dosya kapsama. |

İlk deneylerde tüm çapraz kombinasyonları çalıştırmak gerekmiyor. Amaç, önce temsil ailelerinin uygunluğunu görmek; daha sonra veri ve donanımın izin verdiği adayları daraltmaktır. **Bu rapor herhangi bir sütundaki seçeneği nihai karar olarak işaretlemez.**

## 10. Tarama yöntemi ve sınırlar

Aramalar kişisel bilgi erişimi, çok dilli temsil, diller arası değerlendirme, sıralama birleşimi, parça–dosya toplama, vektör indeksleri ve RAG/uzun bağlam maliyet karşılaştırması eksenlerinde yapıldı. Örnek sorgular: `personal information retrieval Stuff I've Seen`, `multilingual E5 technical report`, `BGE M3 cross lingual retrieval`, `MIRACL multilingual retrieval`, `NeuCLIRBench`, `PARADE passage aggregation`, `ColBERT late interaction`, `SPLADE sparse lexical`, `RAG long context comprehensive study`, `Turkish information retrieval benchmark`, `TR-MTEB`, `TR-TEB`, `TurkColBERT`, `RAGTurk`.

Birincil kaynaklara öncelik verildi: ACL Anthology, arXiv yazar kayıtları, yayıncı/yazar PDF’leri, araştırma kurumları, resmî dokümantasyon ve proje depoları. Blog/forum özetleri bilimsel kanıt olarak kullanılmadı. Yazılım örnekleri hakemli çalışmalarla aynı kanıt düzeyinde değerlendirilmedi.

Bu, bütün literatürü kapsayan sistematik derleme veya meta-analiz değildir. Kaynak bazında inceleme düzeyi kaynakçada belirtilmiştir. Nicel sonuçlar yeniden üretilmedi; model veya sistem kurulmadı. Özellikle eşleşme yokluğu, açıklamaların doğrulanması ve Türkçe–İngilizce kişisel not veri kümesi için daha derin araştırma gerekir. Bu açık noktalar yöntem seçiminin girdileridir; tamamlanmış çözüm diye sunulmaz.
