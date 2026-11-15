# NLP Tabanlı Çok Dilli Bellek Kaynağı Bulma Sistemi

**Durum:** Proje kapsamı belirlendi; yöntem araştırması ve uygulama henüz başlamadı.  
**Tarih:** 12 Kasım 2026  
**Belgenin amacı:** Problemi, üzerinde anlaşılan kapsamı, araştırma hipotezini ve ilk çalışan sürüme giden yol haritasını tek yerde açıklamak.

## 1. Projenin özeti

Bu proje, yapay zekâ araçlarının kullandığı büyük metin tabanlı bellek depolarında, gelen bir sorguyla ilgili kaynak dosyalarını bulmayı amaçlar. Markdown ve düz metin dosyaları önceden indekslenir. Sorgu geldiğinde NLP tabanlı eşleştirme ile ilgili dosyalar sıralanır; dosya yolları, eşleşme puanları ve eşleşmeyi açıklayan kelime veya ifadeler döndürülür.

Sistem kaynağın içeriğinden nihai cevap üretmez. Sonuçları alan yapay zekâ aracı, ihtiyaç duyduğu dosyaları verilen yollardan okuyabilir. İlk sürüm yerelde çalışan bir komut satırı aracı olacaktır. Belirli bir yapay zekâ ürününe bağlı olmayacak; API veya MCP entegrasyonu ileride değerlendirilecektir.

## 2. Problem tanımı

### 2.1. Büyük bellek depolarında ilgili kaynağı bulma

Projenin çıkış noktası, çok sayıda `.md` dosyası içeren bellek depolarında gerekli bilgiyi bulmak için dosyaların geniş ölçüde okunmasına ihtiyaç duyulmasıdır. Bu durumun her sistemde zorunlu olduğu varsayılmamaktadır; mevcut arama davranışı ve maliyeti deneylerle incelenecektir.

Bir sorgu yalnızca birkaç dosyayla ilgili olsa da kaynakları bulmak için çok daha fazla içeriğin işlenmesi gerekebilir. Ayrıca modele gereğinden fazla içerik verilmesi, ilgili bilginin seçilmesini zorlaştırabilir. Proje bu iki maliyeti ayrı ele alır:

- **Arama maliyeti:** İlgili dosyaları belirlemek için okunan veri ve harcanan süre.
- **Aktarım maliyeti:** Kaynak seçimi sırasında sorguyu gönderen araca döndürülen içerik miktarı.

### 2.2. Dil ve ifade farklılıkları

Sorgu ile kaynak aynı dilde olmayabilir. Örneğin Türkçe sorulan “Veritabanı tercihimiz ve gerekçesi neydi?” sorusunun cevabı İngilizce bir karar notunda bulunabilir. Aynı dilde de farklı kelimelerle aynı konu ifade edilebilir.

Bu nedenle sistemin yalnızca birebir kelime eşleşmelerini değil, sorgu ile kaynak arasındaki anlam ilişkisini de değerlendirmesi hedeflenir. İlk dil kapsamı Türkçe ve İngilizcedir; diğer dillerde başarı iddiası yoktur.

### 2.3. Değişen kaynaklar ve güvenilir sonuçlar

Yeni eklenen veya değiştirilen dosyaların indekse yansıması, silinen dosyaların sonuçlardan çıkarılması gerekir. Ayrıca her sorgunun depoda bir karşılığı bulunmayabilir. Sıralamanın en üstündeki dosya sırf birinci olduğu için ilgili kabul edilmemelidir.

## 3. Amaç ve araştırma sorusu

**Amaç:** Yerelde çalışan, araçtan bağımsız bir NLP sistemiyle sorguyu doğru kaynak dosyalarıyla eşleştirmek; bunu yaparken her sorguda bütün kaynakları yeniden okuma ihtiyacını ve kaynak seçimi için aktarılan içerik miktarını azaltmak.

**Temel araştırma sorusu:** Kalıcı indeksleme ve NLP tabanlı eşleştirme, Türkçe ve İngilizce metin depolarında ilgili kaynakları hangi doğruluk ve maliyetle bulabilir? Sorgu ile kaynağın farklı dillerde olması sonuçları nasıl etkiler?

## 4. Araştırma hipotezi

> Kalıcı bir indeks ve NLP tabanlı eşleştirme kullanılarak, her sorguda bütün kaynak dosyaları yeniden okunmadan ilgili dosyalar bulunabilir. Bu yaklaşım, sorgu ile kaynağın farklı dillerde olduğu durumlarda da yararlı sonuçlar üretirken kaynak bulma sırasında okunan veri miktarını ve sorguyu gönderen araca aktarılan içeriği azaltabilir.

Bu ifade henüz doğrulanmış bir sonuç değildir. Aşağıdaki yönleri deneylerle sınanacaktır:

1. **Kaynak bulma kalitesi:** İlgili dosyaların üst sıralarda bulunması ve ilgisiz sonuçların sınırlandırılması.
2. **Çok dilli erişim:** Türkçe–İngilizce ve İngilizce–Türkçe sorgularda ilgili dosyaların bulunması.
3. **Maliyet:** Kaynak bulma kalitesiyle birlikte sorgu başına okuma, süre ve çıktı boyutunun değerlendirilmesi.
4. **Sonuç vermeme davranışı:** İlgili kaynak bulunmayan sorularda sistemin eşleşme olmadığını bildirebilmesi.

İndeksin ilk oluşturulması için kaynakların okunması gerekir. İndeks oluşturma ve güncelleme maliyeti, sorgu maliyetinden ayrı raporlanacaktır. Maliyeti düşürürken ilgili kaynakları kaçırmak tek başına başarı sayılmayacaktır.

## 5. İlk sürümün kapsamı

| Alan | Kararlaştırılan kapsam |
| --- | --- |
| Kaynak biçimleri | Markdown (`.md`) ve düz metin (`.txt`) |
| Çalışma alanı | Komutun çalıştırıldığı dizin ve alt dizinleri |
| Diller | Türkçe, İngilizce ve iki dilin birlikte bulunduğu belgeler |
| Çalışma ortamı | Öncelikle tamamen yerel çalışma; haricî veya ücretli model servisi gerektirmeme |
| Kullanım | Komut satırından indeks oluşturma, güncelleme ve sorgulama |
| İndeks | Tekrar kullanılabilen kalıcı indeks |
| Güncelleme | Kullanıcının başlattığı işlemle eklenen, değişen ve silinen dosyaları yansıtma |
| Sonuç | En iyi eşleşen dosyaların sıralı listesi ve kaynak bilgileri |
| Eşleşme yokluğu | Yeterince ilgili kaynak bulunmadığında açık bildirim |
| Tutarlılık | Aynı sorgu, indeks, model ve ayarlarda aynı sonuç sırası |

İndeks dosyalarının ve aracın ürettiği çıktıların yeniden kaynak olarak alınmaması gerekir. Dosya dahil etme/hariç tutma kuralları uygulama tasarımında belirlenecektir.

### 5.1. Sonuçların içeriği

Her sonuç için aşağıdaki bilgiler hedeflenir:

- Dosya yolu.
- Sıralamadaki yeri ve eşleşme puanı.
- Kaynakta gerçekten bulunan birebir eşleşen anahtar kelimeler.
- Kaynakta bulunan ve sorguyla anlamca ilişkili olduğu değerlendirilen ifadeler; birebir eşleşmelerden ayrı etiketlenmiş olarak.

Eşleşme puanı kaynağın doğru, güncel veya kesin cevap olduğunu göstermez; doğruluk yüzdesi olarak sunulmaz. Anlamsal ilişki açıklamasının nasıl üretileceği ve doğrulanacağı henüz seçilmemiştir. Açıklamalar kaynakta bulunmayan ifadeleri alıntı gibi göstermemelidir.

Çok dilli bir eşleşmede ortak kelime bulunmayabilir. Bu nedenle birebir anahtar kelime eşleşmesi, sonuç döndürmenin zorunlu koşulu olmayacaktır.

### 5.2. Kapsam dışı konular

- Bulunan kaynaklardan nihai doğal dil cevabı üretmek.
- Bellek notlarını otomatik yazmak, birleştirmek, düzeltmek veya unutmak.
- Çelişen kayıtlar arasında hangisinin geçerli olduğuna otomatik karar vermek.
- PDF, web sayfası ve diğer kaynak biçimlerini doğrudan almak.
- API, MCP, arayüz veya yapay zekâ araçlarına özel eklenti geliştirmek.
- Dosya değişikliklerini arka planda otomatik izlemek.

İlgili çelişkili kayıtlar sonuçlarda bulunabilir; sistem bunlardan birini yetkili kaynak ilan etmez.

## 6. Sistemin sorumluluk sınırı

Sistem kaynak seçimini destekler; çağıran yapay zekâ aracının sonraki okuma davranışını yönetmez. Dosya yollarını alan model, dosyaların tamamını okumayı seçerse bu aşamada oluşan maliyet devam eder.

Dolayısıyla proje iki ayrı iddiayı birbirine karıştırmayacaktır:

1. Arama çekirdeğinin kaynakları daha düşük okuma maliyetiyle bulması.
2. Çağıran araca kaynak seçimi için az miktarda bilgi döndürmesi.

Bunlar, tüm yapay zekâ iş akışının toplam bağlam veya token maliyetinin mutlaka azalacağı anlamına gelmez. Aynı şekilde farklı araçlar sorguyu yeniden yazarsa girdiler değişir; aynı sonucu üretme beklentisi yalnızca aynı girdiler ve aynı sistem durumuyla geçerlidir.

## 7. NLP yaklaşımı ve açık teknik kararlar

Başlangıç araştırma yönü, çok dilli anlamsal eşleştirme ve kalıcı indekslemedir. Ancak belirli bir algoritma veya model seçilmiş değildir.

Yöntem araştırmasında şu sorular ele alınacaktır:

- Metinler nasıl temsil edilmeli ve sorgu–kaynak ilişkisi nasıl puanlanmalı?
- Kelime tabanlı arama, anlamsal arama veya bunların birlikte kullanımı bu ihtiyaçta nasıl karşılaştırılmalı?
- Uzun dosyalar bütün olarak mı, bölümler/parçalar üzerinden mi indekslenmeli? Parça puanları dosya sıralamasına nasıl dönüştürülmeli?
- Hazır yerel bir model yeterli mi; uyarlama veya özel model geliştirme hangi eksiklik için gerekli olabilir?
- Yeterince ilgili sonuç bulunmadığına nasıl karar verilmeli? Eşleşme açıklamaları nasıl üretilecek?

Kümeleme bir gereksinim veya öncelikli yöntem değildir. Kullanılacak yöntemler ihtiyaç, deney sonuçları ve yerel çalışma koşullarına göre seçilecektir. Bu bölüm bir literatür taraması sonucu veya tamamlanmış model karşılaştırması değildir.

## 8. Değerlendirme planı

### 8.1. Veri yaklaşımı

Şu anda büyük ölçekli, kullanıma hazır bir kişisel bellek deposu yoktur. Başlangıçta gerçek kullanım ihtiyaçlarını yansıtan, hassas bilgilerden arındırılmış küçük bir değerlendirme kümesi hazırlanacaktır. Her sorgu için ilgili dosyalar önceden işaretlenecektir.

Küme; aynı dilde sorguları, diller arası sorguları, karışık dilli belgeleri, benzer kelimeler içeren ilgisiz dosyaları ve cevabı depoda olmayan soruları içermelidir. Çelişen notlar ile dosya ekleme/değiştirme/silme senaryoları da değerlendirilecektir.

Ölçek davranışı için ayrıca daha büyük bir koleksiyon kullanılacaktır. Veri kaynağı henüz seçilmemiştir. Yalnızca yapay üretilmiş örnekler veya aynı belgeleri çoğaltmak, gerçek kullanım başarısını göstermek için yeterli kabul edilmeyecektir.

### 8.2. Karşılaştırma ve ölçümler

Karşılaştırmalar çalışan sistemi geliştirmeye hizmet edecektir. İlk adaylar; her sorguda kaynak metinlerini tarayan bir referans yöntem, basit bir kelime tabanlı yöntem ve araştırma sonucunda seçilen NLP yaklaşımıdır. Kesin deney düzeni yöntem araştırmasından sonra belirlenecektir.

| Boyut | İzlenecek ölçümler veya davranış |
| --- | --- |
| İlgili kaynakları bulma | İlk k sonuçta isabet ve ilgili dosyaları kapsama oranı; ilk ilgili sonucun sırası |
| Dil etkisi | Aynı dil ve farklı dil sorgularının ayrı sonuçları |
| Sonuç vermeme | İlgisiz sorularda yanlış eşleşme ve ilgili sorularda yanlış ret |
| Sorgu maliyeti | Okunan veri miktarı, sorgu süresi ve döndürülen çıktı boyutu |
| İndeks maliyeti | İlk oluşturma süresi, güncelleme süresi ve disk boyutu |
| İşlevsel doğruluk | Güncel dosya yolları, silinen kayıtların çıkarılması ve tekrarlanabilir sıralama |

Okunan veri ölçümünde kaynak dosyaları ile indeks verisi ayrı izlenmelidir. “Kaynak dosyalar yeniden okunmadı” sonucu, “diskten hiç veri okunmadı” şeklinde sunulmayacaktır. Süre ölçümlerinde ilk çalıştırma ve önbellek etkileri belirtilecektir.

Puan eşikleri veya model ayarları için kullanılan örneklerle nihai değerlendirme örnekleri ayrılacaktır. Sonuç sayısı, veri büyüklüğü ve sayısal başarı hedefleri deney tasarımında belirlenecek; elde edilen sonuçlara göre geriye dönük başarı ölçütü yazılmayacaktır.

## 9. Yol haritası

| Aşama | Yapılacak çalışma | Çıktı / tamamlanma ölçütü |
| --- | --- | --- |
| 1. Yöntem araştırması | İlgili NLP ve bilgi erişim yöntemlerini; çok dillilik, yerel çalışma ve açıklanabilirlik açısından incelemek | Kaynaklandırılmış yöntem karşılaştırması ve ilk prototip için gerekçeli seçim |
| 2. Veri ve deney tasarımı | Belgeleri, sorguları ve ilgili dosya etiketlerini hazırlamak; referans yöntemleri ve ölçüm koşullarını belirlemek | Tekrar kullanılabilir değerlendirme kümesi ve deney planı |
| 3. Temel prototip | Kaynak okuma, kalıcı indeks, sorgulama ve dosya sıralama akışını kurmak | Yerelde uçtan uca çalışan komut satırı aracı |
| 4. İşlevleri tamamlama | İndeks güncelleme, sonuç vermeme kuralı ve eşleşme açıklamalarını eklemek | Kapsamdaki davranışları karşılayan ilk sürüm |
| 5. Karşılaştırmalı değerlendirme | Doğruluk, dil etkisi ve maliyeti ölçmek; hataları incelemek | Tekrarlanabilir deney sonuçları ve hipotezin desteklenen/desteklenmeyen yönleri |
| 6. İyileştirme ve teslim | Ölçülen eksikliklere göre gerekli değişiklikleri yapmak; kullanım ve sınırları belgelemek | Kullanılabilir sürüm, kurulum/kullanım rehberi ve sonuç raporu |

Yol haritası takvim veya tamamlanmış iş listesi değildir. Araştırma ve deneyler yöntem değişikliğine yol açabilir; amaç ve kapsam değişikliği ise ayrıca kararlaştırılır.

## 10. Başlangıç riskleri ve belirsizlikler

- **Verinin temsil gücü:** Küçük veya yapay bir kümede iyi sonuç almak, büyük gerçek depolarda başarıyı garanti etmez.
- **Dil ve terim farkları:** Teknik terimler, kısa sorgular ve karışık dil kullanımı ayrıca incelenmelidir.
- **Parça–dosya ilişkisi:** Bir dosyanın küçük bir bölümü ilgiliyken bütün dosyayı temsil etmek veya puanlamak yanıltıcı olabilir.
- **Puan ve açıklama güvenilirliği:** Yüksek puan doğruluk kanıtı değildir; açıklamalar gerçek eşleşmeyi olduğundan güçlü göstermemelidir.
- **Yerel kaynaklar ve güncellik:** Modelin donanım ihtiyacı ile indeksin disk maliyeti bilinmiyor; güncelleme yapılmadığında indeks kaynakların gerisinde kalabilir.

## 11. İlk sürümün tamamlanma tanımı

İlk sürüm; belirtilen dizindeki desteklenen dosyaları indeksleyebildiğinde, indeksi güncelleyebildiğinde, Türkçe ve İngilizce sorgular için sıralı dosya sonuçları ve eşleşme bilgileri üretebildiğinde, yeterli eşleşme yokluğunu bildirebildiğinde ve bu davranışları tekrarlanabilir değerlendirmeyle gösterebildiğinde işlevsel olarak tamamlanmış sayılacaktır.

Çalışan bir sürüm üretmek ile araştırma hipotezini doğrulamak ayrı sonuçlardır. Nihai rapor, hangi koşullarda iyileşme sağlandığını, hangi koşullarda sağlanmadığını ve sonraki geliştirmelerin hangi kanıtlara dayandığını açıkça belirtmelidir.
