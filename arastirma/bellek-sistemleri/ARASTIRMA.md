# Yapay zekâ neden belleğe ihtiyaç duyuyor?

Kişisel bilgi bankaları, ajan belleği ve token maliyeti üzerine karşılaştırmalı araştırma. **Tarama tarihi: 12 Kasım 2026.** Bu çalışma problem gerekçesine ve yöntem seçimine girdidir; nihai model veya algoritma seçilmedi.

## 1. Problemin çıkış noktası

**Bilginin saklanması, ihtiyaç anında bulunması ve doğru kullanılması ayrı problemlerdir.** Kişisel not sistemleri ile yapay zekâ belleği bu zincirin farklı halkalarından yola çıkar.

İnsan tarafında sorun, okunan ve deneyimlenen bilginin dağılması, unutulması ve bir sonraki çalışmada yeniden kullanılamamasıdır. Tiago Forte’nin *Building a Second Brain* yaklaşımı bunu yakalama, düzenleme, damıtma ve üretime dönüştürme adımlarıyla ele alır (CODE). Buradaki amaç daha çok dosya biriktirmekten ziyade bilgiyi çalışmaya dönüştürmektir. Bu, bir NLP algoritması veya LLM ürünü değildir. [Forte’nin kendi açıklaması](https://fortelabs.com/blog/basboverview/)

Yapay zekâ tarafında geçmiş konuşma, sıradan bir çıkarım çağrısıyla kendiliğinden model ağırlıklarına yazılmaz. Oturumlar arasındaki devamlılığı uygulamanın sakladığı durum, notlar ve yeniden sağladığı bağlam kurar. **Modelin eğitimden gelen bilgisi, aktif bağlamı ve dış belleği aynı şey değildir.** Mert Cobanov’un anlatımı bu ayrımı etkileşimli örneklerle açar. [How AI Agent Memory Works](https://memory.cobanov.dev/)

Büyük bağlam penceresi tek başına yeterli çözüm değildir: uzun konuşmada gereksiz içerik birikir; özetleme ise sonradan gerekli olacak ayrıntıları kaybedebilir. Anthropic’in mühendislik yazısı bağlam sıkıştırma ve kalıcı not tutmayı bu nedenle ayrı teknikler olarak ele alır. [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**Bu kaynaklardan çıkan problem haritası — araştırmacı yorumu:**

| Baskı | İlk çözüm | Çözümün oluşturduğu yeni ihtiyaç |
| --- | --- | --- |
| İnsan her ayrıntıyı hatırlayamıyor | Haricî not ve kaynak deposu | Dosya adı veya ilk kullanılan kelime bilinmeden erişim |
| Ajan yeni oturumda devam edemiyor | Kalıcı durum ve devir notları | Hangi notların yeni bağlama alınacağını seçme |
| Geçmiş büyüyor | Özetleme ve seçici erişim | Bilgi kaybını ve kaçırılan kanıtı ölçme |
| Bilgi değişiyor | Güncelleme, sürüm ve zaman bilgisi | Eski karar ile güncel kararın ayrılması |
| Her tur daha fazla içerik taşınıyor | İndeks, bütçe ve önbellek | Toplam maliyeti kaliteyle birlikte değerlendirme |

## 2. Hatırladığın üç referans

**Karpathy:** Doğruladığım birincil kaynak, Andrej Karpathy’nin 4 Nisan 2026 tarihli **LLM Wiki** tasarım notu. Hazır bir “Karpathy Memory Bank” paketi olarak tanıtılmıyor. Kastettiğin kaynakla en güçlü eşleşme bu; ad benzerliğinden kesin özdeşlik çıkarmıyorum. [Orijinal gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**Avenox Beyin:** Doğrulanan proje **avenoxai/avenoxbeyin**. Güncel README V3.12.0’ı anlatıyor; kod incelemesi `main` dalının **7eccf32b099c0925d467e2d610cfb4367a4dc3e3** anlık görüntüsüne sabitlendi. `main` içeriği ile yayınlanmış sürüm paketinin birebir aynı olduğu varsayılmadı. [Depo](https://github.com/avenoxai/avenoxbeyin)

**Mert Cobanov:** Yazının tam adı **How AI Agent Memory Works**. Kısa/uzun süreli bellek, anlamsal erişim, bellek türleri, erişim hattı ve üretim sorunlarını anlatan etkileşimli bir eğitim sayfası. Bir bellek ürününün başarı veya maliyet deneyi olarak kullanılmamalı. Örnek gösterimler gerçek ölçüm yerine kavramı açıklıyor. [Yazıyı aç](https://memory.cobanov.dev/)

“Memory Bank” ayrıca **Cline’ın dosya düzeni yaklaşımının**, **MemoryBank** ise Zhong ve arkadaşlarının akademik sisteminin adı. Aşağıda ayrı kayıtlar olarak inceleniyorlar.

## 3. Kim, neyi, nasıl tasarlamış?

Kartlardaki **maliyet yorumu**, mekanizmanın olası sonucudur; açıkça ölçüm denmediği sürece doğrulanmış tasarruf oranı değildir.

### 01 · Karpathy — LLM Wiki

**Aile:** Dosya ve bilgi bankası

**Çıkış hedefi:** Aynı kaynakları her soruda yeniden birleştirmek yerine biriken bir kişisel bilgi tabanı oluşturmak.

**Tasarım:** Değiştirilmeyen ham kaynaklar, LLM’nin düzenlediği bağlantılı Markdown wiki ve çalışma kurallarını belirleyen şema. Kaynak işleme, sorgulama ve bakım döngüleri var. Ajan önce içerik indeksini, sonra ilgili sayfaları okur.

**Maliyet yaklaşımı:** Sentezi kaynak alımında yapmak, sonraki sorularda yeniden kullanmak. Ancak kaynak alımı ve wiki bakımı da model işi gerektirir. Net tasarruf sorgu sıklığına bağlıdır; gist maliyet benchmark’ı sunmaz.

**Ayırıcı sınır:** Hazır ürün veya tek bir arama algoritması değil, uyarlanabilir tasarım deseni. Büyüyen wiki için arama aracı ihtiyacını kendisi de belirtir.

**Kanıt:** Tasarım notu okundu; çalışan kurulum denenmedi. [Karpathy, LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

### 02 · Cline topluluğu — Memory Bank

**Aile:** Dosya ve bilgi bankası

**Çıkış hedefi:** Kodlama ajanının yeni görev veya oturumda proje amacını, kararları ve kaldığı yeri yeniden kurabilmesi.

**Tasarım:** Proje özeti, ürün bağlamı, aktif durum, sistem desenleri, teknik bağlam ve ilerleme için altı temel Markdown dosyası; bunları okuma ve güncelleme talimatları.

**Maliyet yaklaşımı:** Uzun sohbet yerine düzenlenmiş proje durumu taşınır. Fakat belgelenen talimat her görev başında tüm bellek dosyalarını okumayı ister. Dosyalar büyürse tekrarlanan okuma da büyür; seçici bir indeks zorunlu parça değildir.

**Ayırıcı sınır:** Bir dokümantasyon yöntemi; vektör veritabanı veya otomatik öğrenen model değil. Küçük proje belleğinde anlaşılır bir başlangıç, büyük kişisel arşiv için ayrıca erişim tasarımı gerekir.

**Kanıt:** Resmî doküman ve örnek talimat incelendi; maliyet ölçülmedi. [Cline Memory Bank](https://docs.cline.bot/best-practices/memory-bank)

### 03 · Avenox — Beyin V3

**Aile:** Dosya ve bilgi bankası

**Çıkış hedefi:** Kullanıcının notlarını ve iş devamlılığını farklı AI istemcileri arasında, yerel ve taşınabilir biçimde korumak.

**Tasarım:** Kalıcı kaynaklar Markdown; yerel durum ve indeks SQLite. Aktif ajan anlamlandırır ve not yazar. Kaynak, proje, durum ve değişiklik bilgileri erişimi sınırlar. V2’nin arka planda model çağıran derleyicisi V3’ün çalışma biçimiyle karıştırılmamalı. [README ve geçiş açıklaması](https://github.com/avenoxai/avenoxbeyin/blob/7eccf32b099c0925d467e2d610cfb4367a4dc3e3/README.md)

**Kodda görüldü:** `_tokens` sözcük normalleştirir; `_weighted_rank` BM25 puanı hesaplar; `pack_context` karakter bütçesine göre kaynakları paketler. Bu mekanizma tek başına genel anlamsal veya diller arası erişim kanıtı değildir. [İncelenen çekirdek kod](https://github.com/avenoxai/avenoxbeyin/blob/7eccf32b099c0925d467e2d610cfb4367a4dc3e3/template/.claude/scripts/beyin_v3.py#L1496)

**Maliyet yaklaşımı:** Çekirdek yerel işlemler model çağırmaz; eklenen bağlam ve aktif ajanın yazma/okuma işi yine istemci tüketimidir. Normal, ekonomik ve manuel profiller bağlam sıklığını ve boyutunu yönetir. Ayrıntılar maliyet bölümünde.

**Ayırıcı sınır:** Çalışma sürekliliği ile anlamca doğru kaynak bulma ayrı yeteneklerdir. Bu taramada kişisel vault veya uçtan uca başarı testi yapılmadı. [Runtime sözleşmesi](https://github.com/avenoxai/avenoxbeyin/blob/7eccf32b099c0925d467e2d610cfb4367a4dc3e3/docs/v3/RUNTIME.md)

### 04 · Packer ve arkadaşları — MemGPT; Letta’daki devamı

**Aile:** Ajan ve konuşma belleği

**Çıkış hedefi:** Sınırlı bağlamla uzun belge ve çok oturumlu konuşma yönetmek.

**Tasarım:** MemGPT (2023), işletim sistemi belleğinden esinlenerek bağlam içi ve dışı katmanlar arasında araç çağrılarıyla bilgi taşır. Daha çok bilgi saklamak, hepsini aynı anda modele vermeyi gerektirmez. [MemGPT makalesi](https://arxiv.org/abs/2310.08560)

**Sürüm ayrımı:** Letta’nın güncel Agent SDK dokümanı **MemFS** adlı Git destekli dosya belleği anlatıyor: `system/` içeriği her tur bağlama girerken diğer dosyalar gerektiğinde okunur. Arka plan “dreaming” işlemleri konuşmaları inceleyip belleği güncelleyebilir. Eski core/archival memory anlatımıyla bugünkü SDK birebir eşitlenmemeli. [Güncel Letta Memory](https://docs.letta.com/agent-sdk/memory)

**Maliyet yaklaşımı:** Seçici yükleme aktif bağlamı sınırlar; ek okuma, bellek düzenleme ve arka plan model çağrıları toplam hesaba katılmalıdır.

**Ayırıcı sınır:** Ajanın bellek işlemini doğru seçmesi gerekir. Katmanlı depolama, hatasız hatırlama garantisi değildir.

**Kanıt:** Makale özeti ve resmî mimari belgeleri; canlı deneme yapılmadı.

### 05 · Chhikara ve arkadaşları / Mem0 ekibi — Mem0

**Aile:** Ajan ve konuşma belleği

**Çıkış hedefi:** Uzun konuşmalarda kişiselleştirmeyi daha küçük bir bellek bağlamıyla sürdürebilmek.

**Tasarım:** 2025 makalesi bilgi çıkarma, mevcut anıları güncelleme ve erişim hattını; ayrıca grafik varyantını anlatır. Güncel `add` dokümanı ise eklemeli saklama tarif eder: yeni anılar eklenir, bu işlem mevcut kayıtları silmez veya üzerlerine yazmaz. Tarihsel mimariyle güncel API davranışı eşitlenmemeli. [Güncel Add Memory belgesi](https://docs.mem0.ai/core-concepts/memory-operations/add)

**Maliyet yaklaşımı:** Her sorguda tüm geçmiş yerine seçilmiş anıları taşımak. Bellek çıkarma ve güncelleme maliyeti ayrıca hesaba katılmalı.

**Ayırıcı sınır:** Kısa bağlamın kalite karşılığı 6. bölümde.

**Kanıt:** Belge ve makale incelemesi; hizmet testi değil. [Mem0, v1](https://arxiv.org/html/2504.19413v1)

### 06 · Rasmussen ve arkadaşları / Zep — Graphiti

**Aile:** Bağlantılı ve zamansal bellek

**Çıkış hedefi:** Konuşma ve iş verisi değişirken ilişkileri ve tarihsel bilgiyi birlikte korumak.

**Tasarım:** Bölümlerden varlık ve ilişkiler çıkaran zamansal bilgi grafiği. Bilginin sistemde kaydedildiği zaman ile dünyada geçerli olduğu zaman ayrılır; geçersizleşen ilişkiler işaretlenir.

**Maliyet yaklaşımı:** İlgili ilişkileri ve bağlamı seçerek okumayı daraltmak. Buna karşılık varlık çıkarma, birleştirme ve grafiği güncel tutmanın işlem/model maliyeti vardır; maliyet yalnız sorguda oluşmaz.

**Ayırıcı sınır:** “Hangi tarihte doğruydu?” sorusu için anlamlı bir tasarım. Grafiğe hatalı çıkarım yazılırsa yapılandırılmış olması onu doğru yapmaz.

**Kanıt:** 2025 mimari makalesi, zamansal çıkarma ve geçersizleştirme bölümleri okundu; güncel bulut ürününün maliyet testi yapılmadı. [Zep makalesi](https://arxiv.org/html/2501.13956v1)

### 07 · LangChain — LangMem

**Aile:** Ajan ve konuşma belleği

**Çıkış hedefi:** Uygulama geliştiricisine bilgiyi saklama, güncelleme ve davranışa aktarma bileşenleri sağlamak.

**Tasarım:** Bilgi/profil belleği, deneyim örnekleri ve davranış kuralları ayrılır. Bellek konuşma sırasında veya konuşmalar arasında arka planda oluşturulabilir; kayıtlar birleştirilebilir, güncellenebilir veya kaldırılabilir.

**Maliyet yaklaşımı:** Arka plan işleme kullanıcı yanıtındaki beklemeyi azaltabilir. Bu işlem ücretsiz hale gelmez; model çağrısı yalnız farklı zamanda yapılır. Profilin tamamını taşımak ile koleksiyondan seçici erişim farklı bütçeler doğurur.

**Ayırıcı sınır:** Hazır kişisel not uygulamasından çok geliştirici araç takımı. Sonucun niteliği seçilen depoya, modele, bellek talimatlarına ve çağrı politikasına bağlıdır.

**Kanıt:** Resmî kavramsal rehber incelendi. [LangMem Core Concepts](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/)

### 08 · Xu ve arkadaşları — A-MEM

**Aile:** Bağlantılı ve zamansal bellek

**Çıkış hedefi:** Belleği sabit bir kayıt deposu olmaktan çıkarıp yeni deneyimlerle ilişkileri gelişen bir yapıya dönüştürmek.

**Tasarım:** Zettelkasten’den esinlenen notlar; bağlamsal açıklamalar, anahtar kelimeler ve etiketler. Yeni kayıt önceki anılarla bağlantı kurar; geçmiş kayıtların temsilleri de güncellenebilir.

**Maliyet yaklaşımı:** Bağlantılar gelecekte erişimi kolaylaştırabilir. Ancak not üretimi, bağlantı kararı ve eski notları güncelleme model maliyeti getirir. Ucuz sorgu, ucuz bellek oluşturma anlamına gelmez.

**Ayırıcı sınır:** Karpathy’nin insan tarafından gezilen wiki deseniyle akraba bir fikir taşısa da aynı sistem değildir; deneysel ajan belleği mimarisidir.

**Kanıt:** Makalenin mimari açıklaması incelendi; deneyler tekrarlanmadı. [A-MEM, 2025](https://arxiv.org/abs/2502.12110)

### 09 · Park ve arkadaşları — Generative Agents

**Aile:** Ajan ve konuşma belleği

**Çıkış hedefi:** Sanal ortamda geçmiş deneyimlerine uygun davranan, plan kuran inandırıcı ajanlar oluşturmak.

**Tasarım:** Doğal dilde olay akışı, bu olaylardan çıkarılan üst düzey değerlendirmeler ve planlama. Erişim puanı yakın zamanda erişilmiş olmayı, önem derecesini ve anlamsal ilgiyi birleştirir.

**Maliyet yaklaşımı:** Bağlama sığan üst sıralı anılar seçilir. Önem puanlama ve değerlendirme üretme de model kullanır; sistemin ana hedefi token ekonomisi değildir.

**Ayırıcı sınır:** İnsan benzeri davranış simülasyonu, kişisel arşivde doğru kanıt bulmayla aynı başarı ölçütü değildir. “Önemli” veya “yakın zamanda görülmüş” anı, sorunun doğru kaynağı olmayabilir.

**Kanıt:** 2023 makalesinin bellek erişimi bölümü incelendi. [Generative Agents, §4.1](https://arxiv.org/html/2304.03442v2)

### 10 · Zhong ve arkadaşları — MemoryBank

**Aile:** Ajan ve konuşma belleği

**Çıkış hedefi:** Uzun süreli kişisel sohbetlerde kullanıcının geçmişini ve özelliklerini hatırlayan bir eşlikçi oluşturmak.

**Tasarım:** Geçmiş etkileşimlerden bellek ve kullanıcı bilgisi üretme, ilgili anıları çağırma, zaman ve önemle ilişkili unutma/güçlendirme. Ebbinghaus unutma eğrisinden esinlenir; SiliconFriend örneğiyle sunulur.

**Maliyet yaklaşımı:** Seçici hatırlama ve unutma taşınacak bilgiyi sınırlayabilir. İncelenen özet, bizim kullanımımız için uçtan uca token tasarruf oranı kanıtlamaz.

**Ayırıcı sınır:** İnsan benzeri unutma, güvenilir belge arşivinde istenen davranış olmayabilir. Cline Memory Bank ve Karpathy LLM Wiki ile aynı proje değildir.

**Kanıt:** 2023 arXiv kaydı ve özeti; ayrıntılı kod/deney denetimi yapılmadı. [MemoryBank](https://arxiv.org/abs/2305.10250)

### 11 · Fang ve arkadaşları — LightMem

**Aile:** Verimlilik ve erişim

**Çıkış hedefi:** Bellek sisteminin kendi oluşturma ve güncelleme işlemlerinin aşırı maliyetini azaltmak.

**Tasarım:** Hafif ön sıkıştırma ve konu gruplama; kısa süreli bellekte özetleme; uzun süreli bellekte çevrimdışı birleştirme. İncelenen deneyde LLMLingua-2 ön sıkıştırıcı kullanılır.

**Maliyet yaklaşımı:** Her küçük etkileşimde pahalı bakım yerine daha az içerikle, gruplanmış işlemler yapmak. Bakımı yanıt yolundan ayırmak gecikmeyi azaltabilir; bilgi kaybı ve bakım maliyeti yine ölçülmelidir.

**Ayırıcı sınır:** Buradaki çalışma **2510.18866** numaralı makaledir; aynı adı kullanan başka yayınlarla karıştırılmamalı. Sayısal sonuçların ölçüm kapsamı 6. bölümde açıklanıyor.

**Kanıt:** 2025 v1 yöntem ve deney/maliyet bölümleri incelendi. [LightMem makalesi](https://arxiv.org/html/2510.18866v1)

### 12 · tobi / QMD — Yerel kaynak erişimi

**Aile:** Verimlilik ve erişim

**Çıkış hedefi:** Markdown notları, belgeler ve bilgi tabanlarını cihaz üzerinde aranabilir hale getirmek.

**Tasarım:** BM25, vektör araması, sorgu genişletme, sıra birleştirme ve yerel LLM yeniden sıralaması. CLI ve MCP çıktıları; dosya yolu, kısa sonuç ve gerektiğinde satır aralığıyla içerik alma seçenekleri.

**Maliyet yaklaşımı:** Önce kaynak seçmek, sonra gerekli içeriği almak; yerel modellerle dış API kullanımını azaltmak. Yerel hesaplama, model belleği ve indeksleme maliyeti ortadan kalkmaz.

**Ayırıcı sınır:** Kişisel belleği baştan sona yöneten sistemden çok erişim bileşeni. Projemize doğrudan yakın bir karşılaştırma örneği; Türkçe–İngilizce başarısı bu taramada doğrulanmadı.

**Kanıt:** Güncel depo README’sinin mimari ve çıktı seçenekleri incelendi; kurulum, kod denetimi ve benchmark yapılmadı. [QMD](https://github.com/tobi/qmd/blob/main/README.md)

## 4. Temel farklar aynı tabloda

Bu tablo yukarıdaki kaynakların **nitel sentezidir**, başarı sıralaması değildir. Sistemler farklı hedeflere ve olgunluk düzeylerine sahiptir.

| Yaklaşım | Asıl saklanan şey | Belleği kim düzenler? | Bağlama taşıma ilkesi | Ana maliyet riski |
| --- | --- | --- | --- | --- |
| LLM Wiki | Kaynaklardan sentezlenmiş bilgi | Ajan, kullanıcı yönlendirmesiyle | İndeks → ilgili sayfalar | Sentez ve bakım tekrarı |
| Cline | Proje amacı ve çalışma durumu | Kodlama ajanı | Bellek dosyalarını yeniden okuma | Büyüyen dosyalar |
| Avenox V3 | Not, kaynak, görev, devir kaydı | Aktif ajan + yerel motor | Filtreli arama ve sınırlı bağlam | İstemciye eklenen metin |
| MemGPT / Letta | Ajanın kalıcı durumu | Ajan ve bellek araçları | Katmanlar / gerektiğinde dosya | Ek araç ve bakım çağrıları |
| Mem0 | Seçilmiş konuşma bilgileri | Çıkarma ve güncelleme hattı | İlgili anıları getirme | Bellek çıkarma maliyeti |
| Zep / Graphiti | Zamanlı varlık ve ilişkiler | Grafiği güncelleyen hat | İlişkili grafik bağlamı | Grafik oluşturma |
| LangMem | Profil, örnek, davranış bilgisi | Yapılandırılmış bellek işlemleri | Profil veya koleksiyondan erişim | Sıklık ve arka plan işleri |
| A-MEM | Birbirine bağlı anı notları | Bellek düzenleyen model | İlişkili notlar | Bağlantı ve temsil güncelleme |
| Generative Agents | Olaylar ve değerlendirmeler | Simülasyon ajanı | İlgi + önem + erişim yakınlığı | Değerlendirme üretimi |
| MemoryBank | Geçmiş ve kullanıcı bilgisi | Bellek güncelleme hattı | Seçici hatırlama | Özetleme / bilgi kaybı |
| LightMem | Sıkıştırılmış, gruplanmış anılar | Aşamalı bellek hattı | İşlenmiş bellekten erişim | Sıkıştırma–kalite dengesi |
| QMD | Kaynak belgelerin indeksi | İndeksleyici; kaynak ayrı | Sıralı sonuç → içerik | Yerel model ve indeks |

**Saklama yeri ile modelin çalışma yeri ayrı sorulardır.** Markdown’ın yerelde bulunması, onu okuyan ajan bulut modeliyse içeriğin cihazdan hiç çıkmadığı anlamına gelmez. Tersine yerel arama, her sorguda ücretli üretici model gerektirmeyebilir. Bu ayrım ürün seçimi ve maliyet değerlendirmesinde ayrıca kontrol edilmelidir.

## 5. Token maliyetini nasıl azaltıyorlar?

### Maliyeti hangi aşamaya taşıdıklarını izle

**Seçici erişim:** Bütün geçmiş yerine kısa bir kanıt kümesi taşıma. Az sonuç döndürmek ucuz olabilir; doğru kaynağı kaçırmak ise ek aramalara yol açabilir. Mem0, QMD ve katmanlı bellek örnekleri bu açıdan incelenebilir.

**Önceden işleme ve biriktirme:** Kaynağı bir kez anlamlandırıp sonraki sorularda kullanma. Wiki oluşturma ve notlar arası bağlantı bunun örnekleridir. Az tekrar kullanılan veya sürekli değişen bilgi için ilk yatırım geri kazanılamayabilir.

**Sıkıştırma ve bakım sıklığı:** Geçmişi özetleme, ilgisiz araç çıktısını çıkarma, işlemleri gruplama. Özetin kalitesi ile boyutu birlikte değerlendirilmelidir. Arka plana taşınan iş, kullanıcı gecikmesini azaltabilir ama token tüketmeye devam eder. [Anthropic: bağlam sıkıştırma ve araç sonucu temizleme](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)

**Yerel işlem ve açık bağlam bütçesi:** Avenox V3’ün belgelenen normal profili en çok 5.000 karakterlik ek bağlam; ekonomik profili yalnız oturum başında en çok 2.000 karakter ve en az 15 dakika kontrol aralığı kullanır. Manuel profil otomatik işlemleri kapatır. Bunlar **karakter sınırıdır, token kotası değildir**; açılış belleği ve istemci sınırları için ayrı ayarlar da vardır. %60 daha az karakter tavanı, %60 daha az toplam fatura demek değildir. [Avenox tercihleri](https://github.com/avenoxai/avenoxbeyin/blob/7eccf32b099c0925d467e2d610cfb4367a4dc3e3/docs/v3/PREFERENCES.md)

**Önbellekleme:** Değişmeyen prompt ön ekini yeniden hesaplamamak maliyet ve gecikmeyi azaltabilir. Ön ek değişimi ve süre sonu cache isabetini etkiler. Bu, doğru anıyı seçme mekanizması veya kalıcı bilgi bankası değildir. [Anthropic’in maliyet ve cache açıklaması](https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform)

### Toplam maliyet hesabı

Aşağıdaki ifade belirli bir sağlayıcının fiyatı değil, **bu araştırma için maliyet muhasebesi çerçevesidir**:

```text
Toplam maliyet = ilk hazırlık + güncelleme/bakım + tüm sorguların maliyeti

Her model çağrısı =
  (normal giriş tokenı × giriş fiyatı
   + cache okuma tokenı × cache okuma fiyatı
   + cache yazma tokenı × cache yazma fiyatı
   + çıkış tokenı × çıkış fiyatı) / 1.000.000

Ayrıca: embedding + yeniden sıralama + araç çağrıları
        + yerel hesaplama/depolama + başarısız erişim sonrası tekrarlar
```

Fiyatlar milyon token başına tanımlandığında bu formül geçerlidir. Normal, cache okuma ve cache yazma miktarları çift sayılmadan ayrılmalı; farklı modellerin çağrıları kendi fiyatlarıyla toplanmalıdır. Abonelik kotası, yerel enerji/zaman maliyeti ve API faturası aynı ölçü birimi değildir.

**Temsili amortisman örneği — ölçülmüş sonuç veya fiyat teklifi değil:** Aynı kaliteyi sağlayan iki yöntemde her sorgunun ilgili giriş bölümü 20.000’den 2.000 tokena insin. Hazırlık işlemi aynı birim maliyette 180.000 ek giriş tokenı gerektirsin; çıkış, cache ve güncelleme farkı olmasın. Sorgu başına 18.000 token fark oluşur; **10 sorguda başa baş**, 11. sorgudan itibaren net kazanç olur. Çıkış tokenı veya bakım maliyeti artarsa bu eşik değişir.

**Bizim projede ayrı ölçülecekler:** İndeks oluştururken okunan kaynak; sorguda okunan indeks ve kaynak; araçtan dönen çıktı; sonradan ajanın okuduğu dosyalar; bunların kaç model çağrısında tekrar taşındığı. Dosya yolunu kısa döndürmek, ajanın daha sonra büyük dosyaları okumasını ücretsiz yapmaz.

## 6. Sayısal iddiaların kanıtı ve sınırı

### Mem0: Daha kısa sorgu bağlamı, kalite karşılığıyla birlikte

2025 v1 makalesi, LoCoMo ve GPT-4o-mini düzeninde şu değerleri raporluyor:

| Yöntem | Sorguya getirilen bağlam tokenı | LLM-as-judge skoru | Toplam p95 yanıt süresi |
| --- | ---: | ---: | ---: |
| Tam geçmiş | 26.031 | %72,90 | 17,117 sn |
| Mem0 | 1.764 | %66,88 | 1,440 sn |

Tablodan hesaplanan bağlam azalması yaklaşık **%93,2**. Ancak kalite skoru da daha düşük. Buradaki token ölçümü **erişimden gelen bağlamı** sayıyor; bellek oluşturma/güncelleme, bütün çıkışlar ve cache dahil toplam faturanın aynı oranda düşeceğini kanıtlamıyor. Bunlar yazarların sonuçları; bu taramada yeniden çalıştırılmadı. [Mem0, §3.2 ve Tablo 2](https://arxiv.org/html/2504.19413v1)

### LightMem: Bellek bakım maliyetinin azaltılması

v1 çalışması LongMemEval-S üzerinde GPT-4o-mini ve Qwen3-30B-A3B-Instruct-2507 kullanır; özetleme ve güncellemenin giriş/çıkış tokenlarını, çağrılarını ve süresini ölçer. Bazı karşılaştırmalarda yaklaşık **117 kat** token azalması bildirilir. **Sonraki retrieval ve soru-cevap maliyeti özellikle bu hesaba dahil edilmemiştir.** Sonuç baseline, sıkıştırma oranı ve tampon eşiğine bağlıdır. Mem0’un sorgu bağlamı yüzdesiyle aynı eksene konamaz. [LightMem, Tablo 1 ve §4.1](https://arxiv.org/html/2510.18866v1)

### Diğer örneklerde ne biliyoruz?

Cline, Karpathy ve QMD için incelenen belgeler mekanizmayı anlatıyor; bu tarama üzerinden evrensel tasarruf yüzdesi verilemez. Avenox’un karakter sınırları yapılandırma bilgisidir. Bu dört örnek için kendi Türkçe–İngilizce veri kümemizde eşit kalite altında maliyet ölçülmedi.

Bir karşılaştırma kullanılmadan önce **veri kümesi, sürüm, üretici model, değerlendiren model, belleği oluşturma biçimi, ölçülen aşama ve kalite metriği** birlikte kaydedilmelidir. Farklı deneylerin en iyi sayılarını toplayıp ürün sıralaması yapmak yanıltıcı olur.

## 7. Bizim araştırmamız için neyi gerekçelendiriyor?

**Sentez:** Bellek sistemleri çoğaldıkça kalıcı bilgi depoları oluşuyor. Bu depoların büyüklüğü, ifade çeşitliliği ve dil farklılığı, depolamadan ayrı bir kaynak erişimi problemi doğuruyor. Projemiz bu sistemlerin tamamını yeniden kurmayı değil, yerel metin depolarında ilgili dosyaları bulmayı ele alıyor. [Mevcut proje kapsamı](../../PROJE_TANIMI.md)

Bu tarama şu iddiayı desteklemez: “Mevcut sistemler her sorguda bütün dosyaları okumak zorunda.” Karpathy seçici sayfa okuması, Avenox bütçeli erişim, QMD ise doğrudan arama hattı sunuyor. Dolayısıyla araştırma gerekçesi **arama yokluğu** üzerine kurulmamalı.

**Araştırılacak soru:** Mevcut erişim yaklaşımları Türkçe/İngilizce, farklı ifadeyle sorma ve diller arası sorgularda hangi dosyaları kaçırıyor; eşit erişim kalitesinde okuma ve bağlam aktarımı ne kadar azaltılabiliyor?

LongMemEval, bellek başarısını bilgi çıkarma, çok oturumdan akıl yürütme, zaman, bilgi güncelleme ve cevap vermekten kaçınma boyutlarında ele alır. Bu, “buldu mu?” sorusunun tek başına yetmediğini gösterir. Fakat onun konuşma cevabı metriği bizim dosya sıralama metriğimizle aynı değildir. [LongMemEval](https://arxiv.org/abs/2410.10813)

| Senaryo | Erişim açısından incelenecek davranış |
| --- | --- |
| Aynı niyet, farklı kelimeler | Doğru kaynak üst sıralarda mı? |
| Türkçe soru, İngilizce not ve tersi | Ortak kelime olmadan kaynak bulunuyor mu? |
| Benzer iki proje | Yanlış projenin dosyası öne çıkıyor mu? |
| Eski ve yeni karar | Kaynak tarihi/durumu görünür mü; iki kanıt ayırt edilebiliyor mu? |
| Depoda cevabı olmayan soru | Sırf birinci sonuç var diye eşleşme sunuluyor mu? |
| Birden fazla dosyada gerekçe | Gerekli dosyaların tümü getirilebiliyor mu? |
| Değiştirilmiş veya silinmiş not | İndeks güncellemesi sonucu doğru yansıtıyor mu? |

Bu senaryolar değerlendirme girdisidir. Geçerli kararı otomatik seçmek, bellek notu yazmak ve nihai cevap üretmek mevcut ilk sürüm kapsamına eklenmedi. Model, sıralama yöntemi ve indeks tasarımı **kararlaştırılacak**.

## 8. Okuma sırası ve inceleme sınırı

Önce [Mert Cobanov’un etkileşimli anlatımı](https://memory.cobanov.dev/), ardından [Karpathy’nin tasarım notu](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) ile [Cline’ın dosya yaklaşımı](https://docs.cline.bot/best-practices/memory-bank) okunabilir. Sonra [Avenox](https://github.com/avenoxai/avenoxbeyin) ve [QMD](https://github.com/tobi/qmd) ile mevcut yerel erişim seçenekleri; [Mem0](https://arxiv.org/html/2504.19413v1), [LightMem](https://arxiv.org/html/2510.18866v1) ve [LongMemEval](https://arxiv.org/abs/2410.10813) ile ölçümün kapsamı incelenebilir.

**Tarama türü:** Birincil kaynaklara dayalı, amaçlı örneklemle yapılmış karşılaştırmalı başlangıç taraması. Sistematik derleme veya bütün ürünleri kapsayan pazar envanteri değildir. Akademik çalışmalar, uygulanabilir desenler ve araçlar aynı tür kanıt sayılmadı.

**İnceleme düzeyi:** Mert’in sayfası ve Karpathy’nin notu doğrudan okundu. Ürünlerde resmî belgeler kullanıldı. Avenox’ta ayrıca sabit commit üzerinde normalleştirme, BM25 sıralama ve bağlam paketleme kodu okundu. Mem0 ve LightMem’de maliyet bölümünün neyi saydığı kontrol edildi; diğer makalelerde kartlarda belirtilen kapsam izlendi. Hiçbir sistem kurulup karşılaştırmalı olarak çalıştırılmadı; token faturası ve Türkçe–İngilizce erişim başarısı ölçülmedi.

**Güncellik:** Akademik bulgular bağlantıdaki tarih/sürüme aittir; güncel ürün özelliği gibi sunulmamalı. Letta’nın tarihsel MemGPT yaklaşımı ile güncel SDK belgesi ayrıldı. Avenox için eski araştırma notlarına dayanmak yerine güncel depo yeniden kontrol edildi. Belgelerde açıklanan her davranışın canlı istemcide gerçekleştiği ayrıca doğrulanmadı.

Bu bölüm önceki NLP yöntem taramasını tamamlar. [NLP araştırma defterine dön](../index.html).
