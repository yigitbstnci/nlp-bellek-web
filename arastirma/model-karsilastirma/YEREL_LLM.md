# Yerel LLM ile kaynak seçimi — araştırma ve deney önerisi

**14 Kasım 2026 · Belge araştırması ve önerilen protokol. Yerel LLM deneyi henüz yapılmadı.** Nihai yöntem ve model kararlaştırılmadı. Bu çalışma, hazır bir üretici LLM'nin ayrı embedding modeli olmadan kaynak bulma görevinde kullanılıp kullanılamayacağını inceleyecek. Amaç dosya seçmek ve dosyadaki kanıtı göstermek; serbest cevap üretmek değerlendirme hedefi olmayacak.

### Hazır LLM neyi değiştirebilir?

LLM'ye soru ile kimliklendirilmiş kaynak parçaları birlikte verilip ilgililik sırası üretmesi istenebilir. Hazır ağırlıklar kullanılacağı için başlangıçta model eğitimi veya ince ayar gerekmeyecek. LLM de bir NLP modelidir; burada araştırılan ayrım, genel amaçlı üretici LLM ile ayrı bir embedding modelinin kullanım biçimidir.

Sun ve arkadaşlarının **RankGPT** çalışması, talimat verilen üretici LLM'lerin metinleri yeniden sıralama amacıyla kullanılmasını inceler. Bu, yaklaşım için akademik dayanak sağlar; çalışmanın ChatGPT/GPT-4 bulguları Qwen3-4B veya Gemma 3-4B'nin Türkçe–İngilizce başarısını kanıtlamaz. [Sun ve ark., EMNLP 2023](https://aclanthology.org/2023.emnlp-main.923/)

Bir LLM, dosyalar bilgisayarda durduğu için içeriklerini kendiliğinden bilmez. İçeriği uygulamanın modele vermesi veya modelin çağırabileceği okuma/arama araçlarının sağlanması gerekir. İlk deneyde araç kullanan agent yerine sınırları belirli kaynak seçimi ölçülecek; böylece agent döngüsünün etkisi model karşılaştırmasına karışmayacak.

### İlk denemeye aday iki üretici model

| Aday | Doğrulanan yerel dağıtım | İncelenecek yön | Henüz bilinmeyen |
| --- | --- | --- | --- |
| **Qwen3-4B** | Ollama `qwen3:4b`; görülen paket 2,5 GB, Q4_K_M; kısa kimlik `359d7dd4bcda`; Apache-2.0 | Küçük çok dilli üretici model; kaynak kimliği seçme, iki dilde sorgu genişletme ve sıralama | Bu cihazda gecikme, gerçek bellek ve kaynak bulma başarısı |
| **Gemma 3-4B** | Ollama `gemma3:4b`; görülen paket 3,4 GB, Q4_K_M; kısa kimlik `68ceab7e468a`; Gemma kullanım koşulları | Farklı model ailesinden karşılaştırma; deneyde yalnız metin girdisi kullanılacak | Aynı görevde Türkçe–İngilizce başarısı, gecikme ve bellek |

Paket boyutları **indirme boyutudur; çalışma RAM'i değildir**. Tag'ler zamanla değişebilir: deneyde tam yerel manifest kimliği, Ollama sürümü, quantization ve istem şablonu kaydedilecek. Bunlar bütün güncel LLM'lerin kapsamlı listesi veya en iyi iki model iddiası değildir; konuşmada belirlenen iki somut başlangıç adayıdır. [Qwen3-4B dağıtımı](https://ollama.com/library/qwen3:4b), [Gemma 3-4B dağıtımı](https://ollama.com/library/gemma3:4b)

Ollama bir çalıştırma aracıdır; Qwen/Gemma ise modellerdir. Model ve çalıştırıcı indirildikten sonra, bu tasarımın sorgu ve kaynak değerlendirme adımları yerel API üzerinden yürütülebilir. Bağlam kapasitesi ile etkin çalışma ayarı ayrı kaydedilecek: daha büyük bağlamın bellek ihtiyacı artar. Uzun bağlam ilanı, bütün arşivi düşük maliyetle ve hatasız okuyabilme garantisi değildir. [Ollama bağlam ayarı](https://docs.ollama.com/context-length)

### Aynı problem için üç ana düzen

| Düzen | İş akışı | Ayrı embedding modeli | Kritik sınır |
| --- | --- | --- | --- |
| **A · Doğrudan LLM** | Soru + bütün kaynak parçaları → LLM → sıralı dosya kimlikleri ve kanıt | Gerekmeyecek | Koleksiyon bağlama sığmalı; kaynak sayısı ve uzunluğu büyüdükçe okuma maliyeti artabilir |
| **B · BM25 + LLM** | Soru → BM25 ile adaylar → LLM ile yeniden sıralama ve kanıt seçimi | Gerekmeyecek | BM25'in kaçırdığı kaynak ikinci aşamada geri getirilemez |
| **C · Embedding erişimi** | Kaynakları bir kez vektörleştir → sorguyu vektörleştir → benzerliğe göre sırala → kaynak metnini getir | Kullanılacak | Farklı ifade/dil başarısı ve yanlış benzerlikler ölçülmeli |

**Kontrol düzeni:** BM25 tek başına da çalıştırılacak; böylece B'nin başarısındaki değişimin LLM eklenmesinden gelip gelmediği görülebilecek. İlk turda B, özgün sorguyu kullanacak. Ayrı bir **B+ genişletme deneyi**nde LLM Türkçe ve İngilizce alternatif sorgular üretecek; her sorgunun BM25 listeleri sabit RRF kuralıyla birleştirilip aynı sayıda aday seçilecek. Bu ek model çağrısının süresi de toplam maliyete yazılacak. Genişletmenin kazancı varsayılmayacak; hatalı çeviri, özel ad ve terim kayması ayrıca incelenecek.

**Küçük ve büyük koleksiyonlar:** A yalnız bütün metinlerin gerçekten bağlama sığdığı ortak alt kümede B/C ile karşılaştırılacak. Sığmayan koleksiyonda metni sessizce kesmek yerine A için “bu ayarla uygulanamadı” kaydı tutulacak. Bölümlere ayırıp çok çağrıyla seçim yapmak daha sonra ayrı yöntem olarak incelenebilir. B/C'nin bütün koleksiyondaki sonuçları ile A'nın küçük alt kümedeki sonuçları aynı başarı tablosunda eşdeğer deney gibi sunulmayacak.

### LLM'den istenecek çıktı

Model serbest dosya yolu yazmak yerine verilen kaynak kimliklerinden seçecek. Önerilen çıktı sözleşmesi şu yapıda olacak; aşağıdaki JSON bir **biçim örneğidir, model sonucu değildir**:

```json
{
  "no_match": false,
  "ranking": [
    {"source_id": "S07", "chunk_id": "S07-P02", "evidence_quote": "Kaynak parçasındaki birebir metin."}
  ]
}
```

Kimlik dosya yoluna uygulama tarafından çevrilecek. Alıntının ilgili parçada birebir bulunduğu ve kimliğin verilen adaylardan biri olduğu programatik kontrol edilecek. Bu kontrol metnin gerçekten var olduğunu doğrular; soruyla ilgili olduğunu tek başına doğrulamaz. Boş/uydurulmuş alıntı, yinelenen veya aday dışı kimlik ve bozuk JSON ayrı hata sayılacak. Geçersiz sonuç otomatik başarılı kabul edilmeyecek; onarım çağrısı denenirse çağrı sayısı ve süresi raporlanacak.

Ollama'nın JSON Schema çıktısı biçim denetimine yardımcı olabilir; şemaya uymak doğru kaynak seçildiği anlamına gelmez. LLM'nin ürettiği öz güven puanı da kalibre edilmiş doğruluk olasılığı sayılmayacak. Kaynak metinleri veri olarak sınırlandırılacak; içlerinde talimat gibi görünen ifadelerin bulunması ayrıca bir hata senaryosu olacak. [Ollama yapılandırılmış çıktı belgesi](https://docs.ollama.com/capabilities/structured-outputs)

### Karşılaştırma nasıl adil yapılacak?

**Ortak malzeme:** Aynı belge anlık görüntüsü, aynı parça sınırları ve aynı sorgu/ilgili dosya etiketleri kullanılacak. Dosya düzeyinde sıralamada aynı dosyanın farklı parçaları tekrar sonuç sayılmayacak; en iyi parça sırası esas alınacak. İlk LLM deneyi mevcut 36 kaynak/48 soruluk sentetik kümede yapılabilir. Bu veri üzerinde önceden sonuçlar incelendiği için bu aşama geliştirme/pilot sayılacak. Model kararı için sonuçlara bakılmadan ayrılmış, bağımsız kontrol edilmiş sorgular ve “ilgili kaynak yok” örnekleri gerekecek.

**Dil ve zor örnekler:** TR→TR, EN→EN, TR→EN ve EN→TR ayrı raporlanacak. Aynı bilgiye farklı kelimelerle sorulan sorular; olumsuzlama, benzer proje adı, tarih farkı, yakın ama yanlış gerekçe, soruyu cevaplamayan konu benzerliği ve cevapsız sorular kapsanacak. Kaynağın güncelliği ile metnin soruyla ilgisi ayrı etiketler olarak ele alınacak.

**Sabit ayarlar:** B için geliştirme aşamasında aday sayısı 5/10/20 incelenecek; birincil karşılaştırmanın sayısı değerlendirme kümesine geçmeden sabitlenecek. İstem metni, kaynak gösterim biçimi, çıktı limiti, çalışma bağlamı, sıcaklık ve seed destekleniyorsa seed kaydedilecek. Qwen düşünme modu açık/kapalı sonuçları ayrı koşul olacak. Aday sırasının etkisi sabit rastgele sıralamalarla tekrar ölçülecek; aynı sorunun dil çifti ve tekrarları bağımsız yeni örnekler sayılmayacak.

Uzun bağlamda ilgili metnin konumu performansı etkileyebilir. **Lost in the Middle** çalışması bu etkiyi incelemek için akademik gerekçe sağlar; bulguları bu iki yerel modele doğrudan taşımak yerine baş/orta/son konum senaryoları ayrıca denenecek. [Liu ve ark., TACL 2024](https://aclanthology.org/2024.tacl-1.9/)

### Hangi ölçülerle karar verilecek?

| Boyut | Raporlanacak ölçü | Yorum |
| --- | --- | --- |
| Kaynak bulma | Dosya düzeyinde Hit@1, Recall@5 ve MRR; dört dil yönü ayrı | Birden çok doğru dosya varsa hepsi etiketlenecek; mevcut tek etiketli pilotta Recall@5, Hit@5 ile eşdeğer |
| İlk aşama kaybı | B/B+ için aday kümesinde ilgili dosya var mı? | Adaya girmeme ile LLM'nin yanlış sıralaması ayrılacak |
| Eşleşme yok | Ret precision/recall, cevaplı soruda yanlış ret, cevapsız soruda yanlış kaynak seçimi | Retli değerlendirme mevcut cevaplı pilotun skorlarından ayrı sunulacak; yalnız boş liste döndürmek başarılı sayılamaz |
| Kanıt ve biçim | Geçerli kimlik/JSON, birebir alıntı oranı, bağımsız ilgililik kontrolü | Kaynak seçimi ile alıntının varlığı ve ilgisi ayrı ölçülecek |
| Uçtan uca maliyet | p50/p95 duvar saati, ilk yükleme, toplam girdi/çıktı tokenı, çağrı sayısı, tepe bellek | BM25, sorgu genişletme, LLM seçimi, doğrulama ve dosya okuma dahil; indeks kurma/güncelleme ayrıca |

LLM'nin yanıt üretme süresini embedding modelinin yalnız sorgu kodlama milisaniyesiyle doğrudan karşılaştırmayacağız. Her düzenin **uçtan uca kaynak getirme süresi** aynı başlangıç/bitiş sınırlarıyla ölçülecek; alt adımlar ayrıca gösterilecek. Ollama'nın `load_duration`, `prompt_eval_count`, `prompt_eval_duration`, `eval_count` ve `eval_duration` alanları yardımcı ölçümler sağlar; bütün uygulama süresi ayrıca dışarıdan tutulacak. [Yerel chat API ölçüm alanları](https://docs.ollama.com/api/chat)

**Karar kuralı:** Önce kaynak bulma, yanlış ret ve kanıt gereksinimleri belirlenecek; bunları sağlayan düzenler arasında kabul edilebilir hız/bellek değerlendirilecek. Kullanıcıyla bir gecikme veya RAM limiti henüz kararlaştırılmadığından burada keyfî başarı eşiği ya da kazanan ilan edilmiyor. Mevcut embedding tercih puanları LLM'lere aktarılmayacak.

**Tamamlanan iş:** İki yerel üretici adayın resmî dağıtımları ve LLM ile sıralamanın akademik dayanağı incelendi; karşılaştırma protokolü tanımlandı. **Açık iş:** LLM'lerin bu cihazda çalıştırılması, ölçülmesi ve bağımsız değerlendirme verisiyle yöntem kararı. Bu bölüm eklenirken model indirilmedi, LLM çalıştırılmadı ve mevcut embedding sonuçları değiştirilmedi.
