"""Tamamen sentetik, model sonuçları görülmeden tanımlanan küçük tanı kümesi.
Etiketler asistan tarafından yazılmıştır; bağımsız insan anotasyonu değildir.
"""
from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parent
# id, language, passage, same-language query, other-language query
rows = [
('D01','tr','Atlas projesinde hasta kayıtları hassas olduğu için bulut işleme reddedildi. Veriler yalnız kurumun cihazında işlenecek. Kararın nedeni internet kesintisi değil, mahremiyet gereksinimidir.','Atlas hasta verilerini neden dışarıdaki bir servise göndermiyor?','Why does Atlas keep medical records on the institution’s own machine?'),
('D02','tr','Liman sipariş uygulamasında stok düşümü ve sipariş kaydı aynı işlem içinde tamamlanmalı. PostgreSQL seçiminin gerekçesi bu iki değişikliğin birlikte başarılı olması veya birlikte geri alınmasıdır.','Liman uygulamasında veritabanı tercihinin işlemsel gerekçesi neydi?','Why must an order and its stock deduction succeed or fail together in Liman?'),
('D03','tr','Defter arama aracının indeksi yalnız kullanıcı güncelle komutunu verdiğinde yenilenir. Bu işlem yeni ve değişen dosyaları işler, silinen kaynakların eski sonuçlarını kaldırır. Arka planda izleyici çalışmaz.','Defterden sildiğim notun arama sonucundan çıkması için ne yapmalıyım?','How do I remove deleted notes from Defter search results?'),
('D04','tr','Kuzey servisinde hata günlükleri otuz gün saklanır. Sonrasında günlük içerikleri silinir; toplam hata sayısı gibi kişisel veri içermeyen istatistikler kalabilir.','Kuzeyde eski hata kayıtlarına hangi süre dolunca erişemeyiz?','For how long does Kuzey keep the contents of error logs?'),
('D05','tr','Ada oturum tasarımında erişim belirteçlerinin ömrü on dakikadır. Süre kısa tutulur çünkü çalınmış bir belirtecin kötüye kullanılabileceği pencereyi daraltmak istiyoruz.','Adada oturum anahtarları neden kısa sürede geçersiz oluyor?','Why do Ada access tokens expire after only ten minutes?'),
('D06','tr','Mercek uygulaması fotoğrafları yüklemeden önce en uzun kenarı 1600 piksele indirir. Amaç mobil ağda aktarılacak baytı ve bekleme süresini azaltmaktır; arşivdeki asıl fotoğraf değişmez.','Mercek fotoğraf gönderirken neden çözünürlüğü küçültüyor?','Why does Mercek downscale photos before uploading them?'),
('D07','tr','Fener projesinin yedeklerinden biri farklı bir fiziksel binada tutulur. Aynı binadaki yangın veya su baskınının hem asıl veriyi hem yedeği yok etmesini önlemek hedeflenir.','Fenerin yedeği neden ana sunucuyla aynı yerde tutulmuyor?','Why is one Fener backup stored in another building?'),
('D08','tr','Kıyı asistanında değişmeyen sistem talimatları ön ek önbelleğine alınır. Yeniden kullanım aynı içeriğin tekrar hesaplanmasını azaltabilir. Bu mekanizma eski kararların hangisinin doğru olduğunu seçmez.','Kıyıda sabit yönergelerin tekrar işlenme giderini ne düşürüyor?','What reduces repeated computation of Kıyı’s unchanged system instructions?'),
('D09','tr','Işık sensörünün açma eşiği 300, kapama eşiği 400 olarak ayrıldı. Ölçüm sınır çevresinde dalgalanırken lambanın sürekli açılıp kapanmasını önlemek için histerezis kullanılır.','Sensörde açma ve kapama sınırlarını neden farklı belirledik?','Why does the lamp controller use different switch-on and switch-off thresholds?'),
('D10','tr','Rota uygulamasının ekonomik profilinde ücretli otoyollar dışlanır. En kısa yol birkaç kilometre daha uzun olsa bile geçiş ücreti olmayan güzergâh seçilir.','Ekonomik rota neden bazen daha uzun bir yoldan gidiyor?','Why can the economical route be longer than the shortest route?'),
('D11','tr','Not kutusunda kesinleşmemiş kullanıcı çıkarımları tahmin etiketiyle tutulur. Kullanıcı düzeltirse önceki çıkarım güncel profil bilgisi sayılmaz. Bir tahminin kaydedilmesi onun doğrulandığı anlamına gelmez.','Kullanıcının reddettiği kişisel tahmini sonraki yanıtlarda kullanabilir miyiz?','Should a personal inference rejected by the user still count as current profile information?'),
('D12','tr','Ders çalışma planında sekizinci hafta vize sınavlarına ayrıldı. Bu hafta yeni modül geliştirme işi planlanmadı; önceki konuların tekrarı yapılacak.','Sekizinci haftada neden geliştirme görevi bulunmuyor?','Why are no new development tasks scheduled in week eight?'),
('D13','en','Orion field notes must remain searchable at a conference venue without reliable internet. Offline operation was selected for connectivity resilience; these notes contain no confidential patient information.','Why must Orion notes work without an internet connection?','Orion notlarını internetsiz arayabilmemizin temel gerekçesi nedir?'),
('D14','en','Pebble is a single-user desktop notebook. SQLite was selected to keep deployment simple and avoid running a separate database server. It is not the database chosen for Liman orders.','Why does Pebble use an embedded database rather than a server?','Pebble için ayrıca veritabanı sunucusu kurmama kararını neden aldık?'),
('D15','en','Harbor stores login sessions on the server. Signing out revokes the server-side session immediately, so an old browser token cannot continue to authorize requests.','How does Harbor make logout take effect immediately?','Harborda çıkış yaptıktan sonra eski tarayıcı anahtarının kullanılması nasıl engelleniyor?'),
('D16','en','The journal export tool preserves original file names because existing links refer to those paths. Export compression is a separate option and was not the reason for preserving names.','Why must exported journal notes keep their original names?','Günlük dışa aktarılırken dosya adlarını neden aynen koruyoruz?'),
('D17','en','The research assistant returns brief source excerpts under a fixed context budget. Whole documents can be opened later when needed. This limits the amount of irrelevant text sent during initial source selection.','Why are initial search results short excerpts rather than entire documents?','İlk arama sonucunda bütün belgeyi göndermek yerine neden kısa kaynak parçaları veriyoruz?'),
('D18','en','Nimbus retrieval may return no match when available sources do not support the question. The top-ranked item is not automatically treated as evidence simply because it ranks first.','What should Nimbus do when its notes contain no support for the question?','Nimbusun notlarında soruya dayanak yoksa ilk sonucu yine de sunmalı mı?'),
('D19','en','The tagging prototype assigns each message to a predefined category such as billing or technical support. It does not search a document collection to find evidence for an open-ended question.','What does the message tagging prototype predict?','Mesaj etiketleme prototipi hangi tür çıktıyı tahmin ediyor?'),
('D20','en','Cedar distributes its application to customers. The team checks the exact model license before packaging weights, because permission to download a model does not by itself settle redistribution conditions.','Why does Cedar review licensing before bundling model weights?','Cedarda model ağırlıklarını uygulamayla dağıtmadan önce lisansı neden inceliyoruz?'),
('D21','en','The E5 trial prefixes questions with query and source passages with passage. These markers identify the retrieval roles expected during training, including when the text itself is Turkish.','Why are different role prefixes added to E5 questions and source passages?','E5 denemesinde soruların ve kaynakların başına niçin farklı rol işaretleri ekleniyor?'),
('D22','en','The container cannot read the notes directory because the host folder was not mounted. The fix is to provide the correct volume mapping; changing the embedding model will not grant filesystem access.','Why can the container not see the notes that exist on the host?','Bilgisayarda bulunan not klasörü konteynerin içinden neden görünmüyor?'),
('D23','en','The event graph stores both when a fact was recorded and the period when it was true. This allows the system to distinguish the user’s former address from the current address.','Why does the event graph track validity intervals as well as recording time?','Olay grafiğinde kayıt zamanının yanında geçerlilik aralığını neden tutuyoruz?'),
('D24','en','Checkout retries reuse an idempotency key. If the network drops after payment succeeds, resending the request with the same key must not charge the customer a second time.','How do checkout retries avoid duplicate payments after a connection failure?','Ödeme başarılı olduktan sonra bağlantı koparsa yeniden deneme müşteriden iki kez para çekmeyi nasıl önlüyor?'),
]
documents = [dict(id=i,lang=l,text=t) for i,l,t,_,_ in rows]
queries = []
for i,l,_,same,other in rows:
    for suffix,ql,text in [('a',l,same),('b','en' if l=='tr' else 'tr',other)]:
        queries.append(dict(id=i+'-'+suffix,lang=ql,direction=ql+'-'+l,text=text,relevant=[i],cluster=i))
negatives = [
('N01','tr','Atlasın eski tasarımında bulut işleme önerilmişti. Bu öneri yürürlükte değildir; kararlı internet ve merkezi bakım kolaylığı o zamanki gerekçelerdi.'),
('N02','en','Liman interface colors were chosen for visual consistency. PostgreSQL documentation was linked during the design review, but this note records no database transaction decision.'),
('N03','tr','Defterin arayüz renkleri yeni sürümle güncellenir. Kullanıcı güncelle düğmesine basınca tema dosyaları yenilenir; bu not arama indeksi hakkında değildir.'),
('N04','en','Kuzey retains aggregate service uptime metrics for one year. These metrics contain counts rather than the contents of individual error logs.'),
('N05','tr','Adada kullanıcı parolasının belirli aralıklarla değiştirilmesi zorunlu değildir. Bu tercih, erişim belirteçlerinin on dakikalık süresini uzatmaz.'),
('N06','en','Mercek preserves original photo resolution in the archive so that prints remain sharp. Thumbnail colors are not used for image search.'),
('N07','tr','Fenerde aynı makinedeki ikinci diske her saat kopya alınır. Bu ek kopya fiziksel bina kaybına karşı tek başına yeterli değildir.'),
('N08','en','Kıyı stores the user’s recent decisions in text notes. Correcting these notes updates durable knowledge; it is a different operation from caching an unchanged prompt prefix.'),
('N09','tr','Işık denemesinin ilk sürümünde tek eşik kullanılıyordu ve lamba ölçüm sınırında titriyordu. Bu eski tasarım güncel ayar değildir.'),
('N10','en','Rota’s fastest profile may include toll roads when they reduce travel time. This is a different preference from its economical profile.'),
('N11','tr','Orionda mahrem hasta kayıtları tutulmaz. Konferans notlarının arama ekranı için küçük yazı boyutu seçilmiştir; bu karar ağ bağlantısı gereksinimini açıklamaz.'),
('N12','en','Checkout logs request identifiers for debugging. Logging alone does not make a payment retry idempotent, and it does not guarantee that a customer is charged only once.'),
]
documents += [dict(id=i,lang=l,text=t) for i,l,t in negatives]
pairs = [
dict(id='P01',kind='Türkçe farklı ifade',a='Verileri gizlilik nedeniyle kendi cihazımızda işliyoruz.',b='Mahrem bilgilerin dış sunuculara gitmemesi için yerel işlemeyi seçtik.'),
dict(id='P02',kind='TR–EN yakın anlam',a='Verileri gizlilik nedeniyle kendi cihazımızda işliyoruz.',b='We process sensitive data locally to protect privacy.'),
dict(id='P03',kind='Olumsuzlama',a='Bulut hizmetlerine izin veriliyor.',b='Bulut hizmetlerine izin verilmiyor.'),
dict(id='P04',kind='İlgisiz konu',a='Verileri gizlilik nedeniyle kendi cihazımızda işliyoruz.',b='Bisikletin arka lastiğini değiştirdim.'),
dict(id='P05',kind='Benzer konu, farklı gerekçe',a='Yerel işleme gizlilik için seçildi.',b='Yerel işleme internet bağlantısı olmadığı için seçildi.'),
dict(id='P06',kind='Benzer sözler, farklı proje',a='Atlas projesi PostgreSQL kullanıyor.',b='Orion projesi PostgreSQL kullanıyor.'),
dict(id='P07',kind='Geçmiş ve güncel durum',a='Eski kararımız bulut kullanmaktı.',b='Güncel kararımız bulut kullanmamak.'),
dict(id='P08',kind='İngilizce farklı ifade',a='Retries must not charge the customer twice.',b='Repeated payment requests should not create duplicate charges.'),
]
data = dict(title='TR–EN kaynak erişimi tanı kümesi v1',synthetic=True,independent_annotation=False,documents=documents,queries=queries,pairs=pairs,
limitations=['Asistan tarafından hazırlanmış, bağımsız insan etiketi olmayan küçük sentetik küme.', '24 hedef kaynağın iki dildeki soruları bağımsız 48 örnek sayılmaz.', 'Olumsuzlama ve zaman örnekleri tanı amaçlıdır; doğruluk etiketi olmayan cümle çiftleri başarı metriğine katılmaz.', 'Cevapsız sorgular ve ret eşiği bu deneyde ölçülmez.', 'Kısa paragraflar; büyük arşiv ve uzun dosya başarısı ölçülmez.'])
raw=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
(ROOT/'veri.json').write_text(raw)
(ROOT/'veri.sha256').write_text(hashlib.sha256(raw.encode()).hexdigest()+'  veri.json\n')
print(len(documents),'kaynak;',len(queries),'soru;',len(pairs),'cümle çifti')
