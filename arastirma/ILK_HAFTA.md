# İlk hafta: araştırmaya giriş kaydı

**Tarih:** 12 Kasım 2026  
**Amaç:** Kaynakları toplamak, problemle ilişkilerini kurmak ve yöntem seçimine hazırlanmak.  
**Karar durumu:** Nihai yöntem, algoritma, model, indeks veya kütüphane seçilmedi. Sunumdaki yöntemler başlangıç örnekleridir ve taramayı sınırlandırmaz.

Bu kayıt, mevcut araştırma talebini somutlaştırır. Bağımsız bir resmî haftalık görev listesi doğrulanmadığı için aşağıdaki işler öğretim elemanının kesin haftalık teslim listesi olarak sunulmaz. Proje tanımındaki yöntem araştırması aşamasına giriş niteliğindedir.

## Bu çalışmada tamamlananlar

- [x] Mevcut [proje tanımı](../PROJE_TANIMI.md) okundu; kaynak bulma ile cevap üretme sınırı korundu.
- [x] [26 akademik kaynak ve 6 teknik/uygulamalı kaynak](KAYNAKLAR.md) toplandı; bağlantı, katkı, projeye karşılık, sınır ve inceleme düzeyleri kaydedildi.
- [x] [Yöntem aileleri karşılaştırması](LITERATUR_TARAMASI.md) yazıldı; temsiller, sıralama, indeksleme ve sonuç politikası ayrı kararlar olarak ele alındı.
- [x] Hipotez; indeksleme maliyeti, diller arası kalite, çıktı bütçesi ve sonuç vermeme davranışına ayrıldı.
- [x] Veri ve ölçüm tasarımına giriş için aşağıdaki senaryolar ve kayıt şeması hazırlandı.

Bunlar araştırma hazırlığı çıktılarıdır. Makalelerin tümünün ayrıntılı okunduğu, veri kümesinin hazırlandığı, modellerin çalıştırıldığı veya hipotezin doğrulandığı anlamına gelmez.

## Çalışma problem cümlesi

> Türkçe ve İngilizce kişisel metin depolarında, farklı dil ve ifadelerle sorulan bir bilgi ihtiyacı için ilgili kaynak dosyalarını; erişim kalitesi, güncelleme gereksinimi ve yerel kaynak tüketimi birlikte gözetilerek nasıl bulabiliriz? Önceden oluşturulan indeks ve NLP yöntemlerinin katkıları hangi koşullarda ortaya çıkar?

Bu ifade yöntem belirtmez. Test edilecek olan yalnızca “anlamsal arama çalışıyor mu?” değildir; hangi yaklaşımın hangi sorgu türünde, ne maliyetle yeterli olduğu araştırılır.

## Veri tasarımına başlangıç senaryoları

**Aşağıdaki örnekler tasarım için üretilmiş sentetik senaryolardır.** Gerçek kişisel notlardan alınmadılar; mevcut dosyalar veya ölçülmüş sonuçlar değiller. Bunlar değerlendirme kümesinin yerini tutmaz.

| Senaryo | Örnek sorgu | Hazırlanacak kaynak/etiket durumu | Sınadığı ayrım |
| --- | --- | --- | --- |
| Aynı dilde farklı ifade | “Bütün değişiklikler neden birlikte kaydedilmeli?” | Türkçe işlem atomikliği notu; ortak sözcükleri taşıyan ilgisiz not | Kelime benzerliği / bilgi ihtiyacı |
| TR→EN | “Veritabanını seçmemizin gerekçesi neydi?” | Gerekçeyi yalnızca İngilizce anlatan karar notu | Gerçek diller arası erişim |
| EN→TR | “Why did we stop using the previous storage engine?” | Değişiklik nedenini yalnızca Türkçe anlatan not | Ters yönde diller arası erişim |
| Özel terim | “ERR_CONNECTION_RESET için çözüm notu” | Hata kodunu ve çözümü içeren dosya; benzer hata kodlu karşı örnek | Kesin terim eşleşmesinin önemi |
| Karışık dil | “Deployment sonrası geri dönüş için ne yapıyorduk?” | Türkçe–İngilizce karışık rollback notu | Kod değişimi / karışık dil |
| Yanlış proje | “A projesinde Redis’i neden kaldırdık?” | A ve B projesinde benzer terimler; farklı karar gerekçeleri | Konu benzerliği / proje ilgililiği |
| Birden fazla kaynak | “İlk kararla sonraki değişikliğin gerekçelerini bul.” | İki ilgili dosya; her ikisi de etiketli | İlk sonucu bulmak / ilgili kaynakları kapsamak |
| Kaynak yok | “Hiç kaydetmediğimiz servis için lisans kararı neydi?” | Benzer konulu fakat soruyu karşılamayan dosyalar | Yanlış kabul / sonuç vermeme |
| Uzun dosya | “Denemenin sonundaki iptal gerekçesi neydi?” | Kanıt dosyanın sonunda; başta benzer konu | Kırpma ve parça→dosya sıralaması |
| Güncelleme | Aynı sorguyu indeks güncellemesinden önce/sonra çalıştırma | Dosya ekleme, değiştirme, silme ve yeniden adlandırma | İndeks yaşam döngüsü |

Çelişen iki notun ikisi de sorguya ilgili olabilir. Etiketleme sırasında “arama için ilgili” ile “halen geçerli karar” ayrı tutulmalı; sistemin kapsam dışı olan yetkili kayıt seçimini otomatik yaptığı varsayılmamalıdır.

## Değerlendirme kaydı taslağı

Her sorgu için önerilen alanlar:

| Alan | İçerik |
| --- | --- |
| query_id / intent_group | Sorgu kimliği; çeviri ve paraphrase’lerin ortak niyet grubu |
| query_text / query_language | Gerçek sorgu metni ve dili |
| target_language / scenario | Hedef kaynak dili ve sınanan durum |
| relevant_documents | İlgili dosya kimlikleri, 0/1/2 ilgililik dereceleri ve kısa etiket gerekçesi |
| evidence_location | Kaynak içinde ilgili bölüm veya satır aralığı |
| answerable | Koleksiyonda ihtiyacı karşılayan kaynak var mı? |
| split | Geliştirme, doğrulama veya test |
| corpus_version | Dosya kimliği ve içerik sürümüyle belirlenen koleksiyon durumu |

Bu bir şema taslağıdır, doldurulmuş veri değildir. Etiketler yalnızca modelin ilk sonuçlarından kopyalanmamalı; farklı yöntemlerin adayları bir araya getirilerek insan kontrolü yapılmalıdır. Küçük pilotta ilgili dosyaları kaçırmamak için koleksiyonun tamamı incelenebilir. Aynı niyetin çevirileri/paraphrase’leri farklı bölümlere dağıtılmamalıdır.

## Yöntem kararından önce kalan işler

| İş | Beklenen somut çıktı | Durum |
| --- | --- | --- |
| Öncelikli makaleleri ayrıntılı okuma | Görev, veri, yöntem, karşılaştırma, sınırlılık ve projeye etkisi bulunan okuma kartları | Kaynak bazındaki mevcut okuma düzeyi kaynakçada; derin okuma devam edecek |
| Veri kapsamını belirleme | Kullanılabilir notlar, izin/mahremiyet açısından uygun içerik, dil ve uzunluk dağılımı | Başlanmadı |
| Etiketli pilot hazırlama | Gerçekçi sorgular, benzersiz dosya etiketleri, ayrılmış doğrulama/test grupları | Şema ve senaryolar hazır; veri yok |
| Yerel uygulanabilirliği inceleme | Donanım sınırları, adayların lisansı, bağımlılık ve çevrimdışı çalışma koşulları | Aday kaynaklar toplandı; çalıştırma yok |
| Karşılaştırmayı sabitleme | Referanslar, k/çıktı bütçesi, kalite ölçümleri, maliyet kayıtları ve önceden yazılmış karar ölçütleri | Kavramsal çerçeve hazır; deney ayarları açık |

**Bir sonraki küçük adım:** Kaynakçadaki K01 ve K04’ün tam metinlerini okuyup “kişisel bilgi erişimi” ile “diller arası temsil” için birer okuma kartı çıkarmak. Ardından diğer yöntem aileleri aynı şablonla incelenebilir; bu adım bir model seçimi değildir.

## Okuma kartı şablonu

- Kaynak kimliği, tam künye ve incelenen sayfalar/bölümler:
- Çözdüğü problem ve varsayımları:
- Kullanılan veri; dil içi mi, diller arası mı?
- Temsil, sıralama ve indeksleme yöntemi:
- Karşılaştırmalar; kalite ve maliyet ölçümleri:
- Yazarın gösterdiği sonuç / bizim projeye ilişkin çıkarımımız:
- Sınırlılıklar ve bu projede ayrıca sınanacak nokta:

Kaynak bulma çalışması tamamlandı; proje geliştirme ve deney aşamaları sürüyor. Bu kayıt literatürle yöntem seçimine giriş içindir, ilk çalışan sürümün tamamlanma raporu değildir.
