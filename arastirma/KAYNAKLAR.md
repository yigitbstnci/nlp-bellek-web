# Açıklamalı kaynakça

Tarama tarihi: 12 Kasım 2026. Amaç: yöntem seçimine giriş. **Henüz nihai yöntem, algoritma, model veya kütüphane seçilmedi.** Sunumdaki örnekler seçim dayanağı değildir.

Bu dosya 26 akademik çalışma ile 6 uygulama/dokümantasyon kaynağı içerir. Hakemli yayın, teknik rapor ve yazılım dokümantasyonu ayrı belirtilmiştir. “İnceleme” alanı bu taramada gerçekten erişilen kanıtın düzeyidir; tüm çalışmaların tam metninin ayrıntılı okunduğu veya deneylerinin tekrarlandığı iddia edilmez. Özetler kendi ifadelerimizle yazılmıştır. Yayın sayfasındaki PDF bağlantıları tam metne erişim sağlar; PDF arşivi oluşturulmadı.

## Kişisel bilgi erişimi ve sözcüksel yöntemler

### K01 — Stuff I’ve Seen: A System for Personal Information Retrieval and Re-Use

**Dumais ve ark., 2003 — SIGIR, hakemli konferans.** [Yayın sayfası](https://www.microsoft.com/en-us/research/publication/stuff-ive-seen-a-system-for-personal-information-retrieval-and-re-use/) · [Yazar PDF’i](https://www.microsoft.com/en-us/research/wp-content/uploads/2003/01/siscore-sigir2003-final.pdf)

- **Katkı:** Kişinin daha önce gördüğü belgeleri, e-postaları ve diğer içerikleri ortak bir yerel indeks üzerinden yeniden bulmasını inceler. Zaman ve kişi gibi bağlamsal ipuçlarını değerlendirir.
- **Projeye karşılığı:** Kişisel depolarda kalıcı indeksleme ve tekrar erişimin güçlü bir tarihsel dayanağıdır. İndekslemenin kendisi yeni bir araştırma iddiası olarak sunulmamalıdır.
- **Sınır:** Modern çok dilli embedding veya LLM token tasarrufu deneyi değildir.
- **İnceleme:** Yayın özeti ve PDF’in mimari/indeks güncelleme bölümleri.

### K02 — The Probabilistic Relevance Framework: BM25 and Beyond

**Stephen Robertson ve Hugo Zaragoza, 2009 — Foundations and Trends in Information Retrieval, inceleme çalışması.** [Yayın / DOI](https://doi.org/10.1561/1500000019)

- **Katkı:** Olasılıksal bilgi erişiminin ve BM25 ailesinin kuramsal temelini açıklar.
- **Projeye karşılığı:** Sözcüksel sıralamanın hangi varsayımlarla çalıştığını anlamak ve bir karşılaştırma yöntemi tanımlamak için okunmalıdır.
- **Sınır:** Tek başına sorgu ve belge dilleri arasındaki anlam eşlemesini sağlamaz. Türkçe sözcük biçimleri ve normalizasyon ayrıca değerlendirilmelidir.
- **İnceleme:** Bibliyografik kayıt ve aramada görünen yayıncı PDF kaydı doğrulandı; yayıncı tam metni doğrudan açma isteğine 403 verdi. Ayrıntılı tam metin incelemesi yapılmadı. Uygulama davranışı için U05 ayrıca erişilebilir.

### K03 — Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods

**Gordon V. Cormack, Charles L. A. Clarke ve Stefan Büttcher, 2009 — SIGIR, hakemli konferans.** [Yazar PDF’i](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)

- **Katkı:** Birden fazla sıralamayı ham puanlar yerine sıra konumları üzerinden birleştiren RRF yöntemini değerlendirir.
- **Projeye karşılığı:** Farklı puan ölçekleri üreten yöntemlerin sonuçlarını birleştirmek için adaydır.
- **Sınır:** Birleşim her koleksiyonda üstün değildir; ilgisiz bir listenin katkısı sonucu bozabilir. RRF puanı ilgililik olasılığı değildir.
- **İnceleme:** Yazar PDF’inin yöntem ve deney özeti.

## Çok dilli temsil ve sıralama aileleri

### K04 — Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation

**Nils Reimers ve Iryna Gurevych, 2020 — EMNLP, hakemli konferans.** [Yayın ve PDF](https://aclanthology.org/2020.emnlp-main.365/)

- **Katkı:** Çeviri karşılıklarını ortak bir temsil uzayında yakınlaştırmak için öğretmen–öğrenci eğitimini kullanır.
- **Projeye karşılığı:** Farklı dillerde aynı anlama erişmenin NLP temelini açıklar; hazır model ile uyarlama seçeneklerini anlamaya yardımcı olur.
- **Sınır:** Cümle benzerliği başarısı, kişisel dosyalarda sorgu–belge ilgililiğini veya güncel karar bulmayı doğrudan kanıtlamaz.
- **İnceleme:** Yayın kaydı ve özet.

### K05 — Multilingual E5 Text Embeddings: A Technical Report

**Liang Wang ve ark., 2024 — teknik rapor / arXiv.** [Tam metin](https://arxiv.org/html/2402.05672v1) · [Model kartı](https://huggingface.co/intfloat/multilingual-e5-small)

- **Katkı:** Farklı boyutlarda çok dilli erişim modellerinin eğitimini ve değerlendirmesini açıklar. MIRACL ile bitext mining sonuçlarını ayrı raporlar.
- **Projeye karşılığı:** Yerel kaynak tüketimi ile erişim kalitesini karşılaştırmak için bir model ailesi adayıdır.
- **Sınır:** Eğitim karışımında MIRACL ve Mr. TyDi bulunur; bu veri kümelerindeki sonucu tamamen görülmemiş alana genelleme diye sunmamak gerekir. Çeviri çifti eşleme, doğal bilgi ihtiyacına göre dosya bulma ile aynı görev değildir.
- **İnceleme:** Tam metinde eğitim, değerlendirme tabloları ve model kartının kullanım koşulları.

### K06 — M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation

**Jianlyu Chen ve ark., 2024 — Findings of ACL, hakemli yayın.** [Yayın ve PDF](https://aclanthology.org/2024.findings-acl.137/) · [Model kartı](https://huggingface.co/BAAI/bge-m3)

- **Katkı:** Aynı model ailesinde yoğun, seyrek ve çok vektörlü erişimi; çok dilliliği ve uzun girdileri bir araya getirir.
- **Projeye karşılığı:** Temsil türlerinin karşılaştırılması için güçlü bir araştırma kaynağıdır. BGE-M3 bir adaydır; seçilmiş model değildir.
- **Sınır:** Uzun girdi kabul etmesi dosyanın tamamını tek vektörle temsil etmenin uygun olduğunu göstermez. Model kartında MIRACL sonuçları için düzeltme notu vardır; sürüm/deney ayarı kaydedilmelidir.
- **İnceleme:** Hakemli yayın özeti, PDF’in giriş kısmı ve güncel model kartı.

### K07 — Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models

**Yanzhao Zhang ve ark., 2025 — teknik rapor / arXiv.** [Çalışma](https://arxiv.org/abs/2506.05176)

- **Katkı:** Çok dilli embedding ve yeniden sıralama için 0.6B, 4B ve 8B boyutlarında modeller sunar.
- **Projeye karşılığı:** Daha yeni, farklı kapasitedeki modelleri aday havuzuna dahil eder; embedding ve reranking kararlarını ayırmayı sağlar.
- **Sınır:** Büyük modelin benchmark başarısı yerel cihazda uygun gecikme veya bellek tüketimi sağlayacağını göstermez. Raporun üstünlük iddiaları kendi deney koşullarına aittir.
- **İnceleme:** Yazarların arXiv özeti. Çalıştırılmadı.

### K08 — PARADE: Passage Representation Aggregation for Document Reranking

**Canjia Li ve ark., 2024 dergi cildi; 2023 çevrimiçi yayın — ACM TOIS, hakemli dergi.** [Kurumsal yayın kaydı ve kabul edilmiş metin](https://eprints.gla.ac.uk/298257/) · [arXiv sürümleri](https://arxiv.org/abs/2008.09093)

- **Katkı:** Bir belgenin parçalarından gelen sinyallerin belge sıralamasına nasıl dönüştürüleceğini karşılaştırır. Dağınık kanıt gerektiren ve tek parçada cevaplanan ihtiyaçlar farklı davranır.
- **Projeye karşılığı:** Sonuç birimi dosya olduğu için parça→dosya toplama kuralı başlı başına bir yöntem kararıdır.
- **Sınır:** Makaledeki eğitilmiş toplama modelini küçük kişisel depoya doğrudan taşımak zorunlu değildir; basit maksimum puan gibi yöntemler de adaydır.
- **İnceleme:** Kurumsal özet ve kabul edilmiş metnin deney düzeninden erişilen bölümler.

### K09 — The Faiss library

**Matthijs Douze ve ark., 2024 ilk arXiv sürümü; 2025 revizyonları — teknik çalışma.** [Çalışma](https://arxiv.org/abs/2401.08281)

- **Katkı:** Vektör arama yöntemlerinin hız, bellek ve doğruluk ödünleşimlerini ve Faiss tasarımını açıklar.
- **Projeye karşılığı:** Temsil üretimi ile o temsiller üzerinde arama yapmanın farklı kararlar olduğunu gösterir. Tam tarama ve yaklaşık arama seçeneklerini incelemek için kullanılır.
- **Sınır:** Vektör arama kütüphanesi, dosya sürümü, silme, açıklama ve güncelleme tutarlılığını tek başına çözmez.
- **İnceleme:** arXiv kayıt/özet ve sürüm bilgisi.

### K19 — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT

**Omar Khattab ve Matei Zaharia, 2020 — SIGIR çalışması; erişilen kaynak arXiv.** [Çalışma](https://arxiv.org/abs/2004.12832)

- **Katkı:** Sorgu ve belgeyi ayrı kodlayıp token düzeyindeki etkileşimi daha sonra hesaplar; belge temsilleri önceden üretilebilir.
- **Projeye karşılığı:** Tek vektörlü anlamsal aramanın alternatifidir. Ayrıntılı terim ilişkilerinin katkısı araştırılabilir.
- **Sınır:** Orijinal çalışmadan Türkçe–İngilizce başarı çıkarılamaz; uygun çok dilli model gerekir. Birden fazla vektörün depolama ve arama maliyeti ölçülmelidir.
- **İnceleme:** Yazarların arXiv özeti.

### K20 — SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking

**Thibault Formal, Benjamin Piwowarski ve Stéphane Clinchant, 2021 — SIGIR, hakemli konferans.** [Çalışma](https://arxiv.org/abs/2107.05720) · [Yazar PDF’i](https://www.piwowarski.fr/publication/formal_splade_2021-lwjxesk9/formal_splade_2021-LWJXESK9.pdf)

- **Katkı:** Öğrenilmiş terim ağırlıkları ve genişletmelerle seyrek temsiller üretir; ters indeksle aramayı korur.
- **Projeye karşılığı:** Yöntem alanı yalnızca BM25 ve yoğun embedding seçeneklerinden oluşmaz. Öğrenilmiş seyrek erişim ayrı bir aday ailesidir.
- **Sınır:** Modelin ürettiği genişletme terimleri kaynakta bulunmayabilir; bunlar birebir alıntı gibi sunulamaz. Çok dilli yeterlik ayrı doğrulanmalıdır.
- **İnceleme:** arXiv özeti ve yazar PDF’inin giriş/özet bölümü.

### K21 — Language-agnostic BERT Sentence Embedding

**Fangxiaoyu Feng ve ark., 2022 — ACL, hakemli konferans.** [Yayın ve PDF](https://aclanthology.org/2022.acl-long.62/)

- **Katkı:** LaBSE ile çok dilli cümle temsili ve çeviri çifti erişimini inceler.
- **Projeye karşılığı:** Ortak temsil uzayı yaklaşımının temel çalışmalarındandır; çeviri eşleme ile sorguya ilgili kanıt bulmayı ayırt etmek için okunmalıdır.
- **Sınır:** Bitext başarısı, kişisel notlarda asimetrik soru→belge erişimi başarısı değildir.
- **İnceleme:** Yayın kaydı ve özet.

### K22 — Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs

**Yu. A. Malkov ve D. A. Yashunin, 2016 ilk arXiv sürümü — HNSW temel çalışması.** [Çalışma ve yayın bilgileri](https://arxiv.org/abs/1603.09320)

- **Katkı:** Vektör komşuluğunu katmanlı graf üzerinde yaklaşık aramayla bulur.
- **Projeye karşılığı:** Koleksiyon büyüdüğünde tam vektör taramasının alternatifi olarak incelenebilir.
- **Sınır:** Yaklaşık komşu bulma doğruluğu ile sorguya anlamsal olarak doğru belge bulma doğruluğu farklıdır. Küçük depoda ek indeks karmaşıklığının karşılığı olmayabilir.
- **İnceleme:** Yazarların arXiv özeti. Tarih ilk ön baskı içindir; dergi atfı için bağlantıdaki yayın kaydı kullanılmalıdır.

## Değerlendirme ve veri kümeleri

### K10 — BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models

**Nandan Thakur ve ark., 2021 — NeurIPS Datasets and Benchmarks.** [Hakemli metin](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/65b9eea6e1cc6bb9f0cd2a47751a186f-Paper-round2.pdf) · [arXiv kaydı](https://arxiv.org/abs/2104.08663)

- **Katkı:** Farklı alan ve görevlerde sözcüksel, seyrek, yoğun, geç etkileşimli ve yeniden sıralamalı yöntemleri karşılaştırır. BM25’in güçlü bir referans olabildiğini gösterir.
- **Projeye karşılığı:** Tek veri kümesi veya birkaç kolay örnekle model seçmeme gerekçesidir.
- **Sınır:** Bu deneyler Türkçe–İngilizce kişisel bellek erişiminin doğrudan kanıtı değildir; dönemin modellerine aittir.
- **İnceleme:** Yayın kaydı ve arXiv özeti.

### K11 — Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval

**Xinyu Zhang, Xueguang Ma, Peng Shi ve Jimmy Lin, 2021 — MRL Workshop.** [Yayın ve veri bağlantıları](https://aclanthology.org/2021.mrl-1.12/)

- **Katkı:** On bir dilde, sorguyla kaynağın aynı dilde olduğu erişimi inceler. Deneyde zayıf kalan yoğun modelin hibrite yararlı sinyal ekleyebilmesi dikkat çekicidir.
- **Projeye karşılığı:** İngilizce ve kapsanan diğer dillerde dış değerlendirme adayıdır; hibritin hangi koşulda yarar sağladığını sorgulatır. Türkçe içermez.
- **Sınır:** TR→EN / EN→TR benchmark’ı değildir. Wikipedia’dan kişisel notlara geçiş alan değişimidir.
- **İnceleme:** Yayın özeti, PDF’in görev tanımı/karşılaştırma bölümleri ve [resmî deponun dil listesi](https://github.com/castorini/mr.tydi).

### K12 — MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages

**Xinyu Zhang ve ark., 2023 — TACL, hakemli dergi.** [Yayın ve PDF](https://aclanthology.org/2023.tacl-1.63/)

- **Katkı:** On sekiz dil için insan değerlendirmeli Wikipedia erişim verisi sağlar.
- **Projeye karşılığı:** İngilizce ve kapsanan diğer dillerde dil içi kaliteyi izlemek ve insan ilgililik etiketleme düzenini incelemek için adaydır. Türkçe içermez.
- **Sınır:** Tasarım gereği sorgu ile koleksiyon aynı dildedir. Burada iyi sonuç almak diller arası başarıyı kanıtlamaz.
- **İnceleme:** Hakemli yayın kaydı, özeti ve [resmî deponun dil listesi](https://github.com/project-miracl/miracl).

### K13 — MMTEB: Massive Multilingual Text Embedding Benchmark

**Kenneth Enevoldsen ve ark., 2025 — erişilen kaynak arXiv çalışması.** [Çalışma](https://arxiv.org/abs/2502.13595)

- **Katkı:** Çok sayıda dil ve görev üzerinden embedding değerlendirmesini genişletir.
- **Projeye karşılığı:** Aday model havuzunu ve farklı görevlerdeki davranışı incelemek için yararlıdır.
- **Sınır:** Sınıflandırma, benzerlik ve erişimin toplu ortalaması bu projenin hedef ölçümü değildir. Dil, görev, veri sürümü ve modelin eğitim verisi kontrol edilmelidir. Makaledeki sıralama güncel liderlik tablosu diye sunulamaz.
- **İnceleme:** Yazarların arXiv özeti ve kayıt bilgisi.

### K14 — NeuCLIRBench: A Modern Evaluation Collection for Monolingual, Cross-Language, and Multilingual Information Retrieval

**Dawn Lawrie ve ark., 2025 — erişilen kaynak arXiv ön baskısı.** [Çalışma](https://arxiv.org/abs/2511.14758) · [Veri kartı](https://huggingface.co/datasets/neuclir/bench)

- **Katkı:** Dil içi, diller arası ve çok dilli koleksiyon erişimini ayrı senaryolar olarak sunar. İngilizce sorgular; Çince, Farsça ve Rusça belgeler ile İngilizce çeviriler bulunur.
- **Projeye karşılığı:** Diller arası deneyin nasıl kurulacağı ve çeviri tabanlı erişimin nasıl karşılaştırılacağı için örnektir.
- **Sınır:** Türkçe içermez; proje için doğrudan TR–EN test kümesi olamaz.
- **İnceleme:** arXiv özeti ve veri kartı bilgisi.

## Türkçe için doğrudan ilgili güncel çalışmalar

### K23 — TR-MTEB: A Comprehensive Benchmark and Embedding Model Suite for Turkish Sentence Representations

**Mehmet Selman Baysan ve Tunga Güngör, 2025 — Findings of EMNLP, hakemli yayın.** [Yayın ve PDF](https://aclanthology.org/2025.findings-emnlp.471/) · [Resmî veri/model koleksiyonu](https://huggingface.co/trmteb)

- **Katkı:** Türkçe için erişim dahil altı görev türünde 26 veri kümesini ve Türkçeye özel embedding modellerini sunar; özgün ve çevrilmiş kaynakları birlikte kullanır.
- **Projeye karşılığı:** Türkçe değerlendirme ve aday veri seçimi için doğrudan ilgili bir başlangıç kaynağıdır.
- **Sınır:** Toplu embedding skoru yerine erişim alt görevleri incelenmelidir. Türkçe benchmark olması, TR→EN ve EN→TR kişisel belge erişimini ölçtüğü anlamına gelmez; çevrilmiş verinin etkisi ayrılmalıdır.
- **İnceleme:** Hakemli yayın özeti, PDF’in giriş kısmı ve resmî koleksiyon açıklaması.

### K24 — TR-TEB: Turkish Text Embedding Benchmark

**Ömer Arslan ve ark., 2026 — LREC, hakemli konferans.** [Yayın, PDF ve yazarlar](https://lrec.elra.info/lrec2026-main-862)

- **Katkı:** Beş görev türünde Türkçe embedding değerlendirmesi; açık kaynak, çevrilmiş ve yeni Türkçe veri kümelerini bir araya getirir.
- **Projeye karşılığı:** K23’ten ayrı bir çalışmadır. Erişim verilerini ve değerlendirme düzenini karşılaştırmak, Türkçe değerlendirme havuzunu genişletir.
- **Sınır:** Kişisel not alanına ve diller arası erişime doğrudan genellenemez. Görevler arası ortalama yerine ilgili alt görevler seçilmelidir.
- **İnceleme:** Resmî LREC yayın kaydı ve özet. Yazarların “ilk” nitelemesi özgünlük kanıtı olarak benimsenmedi.

### K25 — TurkColBERT: A Benchmark of Dense and Late-Interaction Models for Turkish Information Retrieval

**Özay Ezerceli ve ark., 2026 — Procedia Computer Science; ön baskı 2025.** [Yayıncı kaydı](https://www.sciencedirect.com/science/article/pii/S1877050926000487) · [Yazar ön baskısı](https://arxiv.org/abs/2511.16528)

- **Katkı:** Türkçe erişimde yoğun kodlayıcılarla geç etkileşimli modelleri, ayrıca indeksleme yöntemlerini karşılaştırır.
- **Projeye karşılığı:** Tek vektörlü modellere erken bağlanmamak ve Türkçe için temsil–indeks maliyetini birlikte incelemek açısından doğrudan ilgilidir.
- **Sınır:** Yazarlar çevrilmiş benchmark’ları ve en fazla 50 bin belgeli deneyleri sınır olarak belirtir. Rapordaki sorgu süreleri bizim donanımımızda beklenen süre değildir; diller arası başarıyı da göstermez.
- **İnceleme:** Yayıncı ve arXiv özetleri; sonuçlar yeniden üretilmedi.

### K26 — RAGTurk: Best Practices for Retrieval Augmented Generation in Turkish

**Süha Kağan Köse ve ark., 2026 — erişilen arXiv kaydında EACL 2026 SIGTURK kabul bilgisi.** [Çalışma](https://arxiv.org/abs/2602.03652)

- **Katkı:** Türkçe RAG hattındaki sorgu dönüşümü, yeniden sıralama ve diğer aşamaları kalite/maliyet açısından karşılaştırır; ek modüllerin her zaman yararlı olmadığını gösterir.
- **Projeye karşılığı:** Türkçe için bileşen katkısını ayrı ölçme ve karmaşıklığın karşılığını sorgulama örneğidir.
- **Sınır:** Tam RAG hattındaki cevap doğruluğu, bizim dosya sıralama başarımızla aynı ölçüm değildir. Üretim modülleri bu projede gereksinim haline gelmez.
- **İnceleme:** Yazarların arXiv özeti ve kabul notu.

## Yapay zekâya kaynak sağlama ve maliyet iddiası

### K15 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**Patrick Lewis ve ark., 2020 — NeurIPS.** [Çalışma](https://arxiv.org/abs/2005.11401)

- **Katkı:** Parametrik model belleği ile dış yoğun indeks üzerinden getirilen bilgiyi birlikte kullanır.
- **Projeye karşılığı:** Haricî bilgi erişiminin yapay zekâya kaynak sağlayabilmesinin temel dayanaklarından biridir.
- **Sınır:** Projemiz cevap üretmiyor. Bu makalenin üretim kalitesi bulguları, bizim dosya seçimi veya toplam token tasarrufumuz olarak aktarılamaz.
- **İnceleme:** Yazarların yayın özeti.

### K16 — Retrieval-augmented generation in multilingual settings

**Nadezhda Chirkova ve ark., 2024 — KnowLLM Workshop.** [Yayın ve PDF](https://aclanthology.org/2024.knowllm-1.15/) · [arXiv](https://arxiv.org/abs/2407.01463)

- **Katkı:** Çok dilli RAG hattında erişim, üretim dili ve değerlendirme sorunlarını birlikte inceler.
- **Projeye karşılığı:** Doğru kaynak bulunması ile çağıran modelin onu doğru kullanmasının ayrı aşamalar olduğunu gösterir.
- **Sınır:** Üretime ilişkin problemler ilk sürümün kapsamı dışındadır; kaynak bulma deneyine doğrudan başarı ölçütü yapılamaz.
- **İnceleme:** Yazarların özet ve yayın kaydı.

### K17 — Lost in the Middle: How Language Models Use Long Contexts

**Nelson F. Liu ve ark., 2024 — TACL; ön baskı 2023.** [Hakemli yayın](https://aclanthology.org/2024.tacl-1.9/)

- **Katkı:** İlgili bilginin uzun bağlam içindeki konumunun, incelenen modellerin başarısını etkileyebildiğini gösterir.
- **Projeye karşılığı:** Seçici kaynak aktarımının araştırılmasını destekleyen motivasyondur.
- **Sınır:** Her güncel model veya her görev için aynı etkiyi kanıtlamaz; kendi başına maliyet tasarrufu sonucu değildir.
- **İnceleme:** Yayın kaydı ve özet.

### K18 — Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach

**Zhuowan Li ve ark., 2024 — EMNLP Industry Track.** [Yayın ve PDF](https://aclanthology.org/2024.emnlp-industry.66/)

- **Katkı:** Kendi deneylerinde yeterli kaynak sağlandığında uzun bağlamın ortalama kalite avantajı, RAG’in ise maliyet avantajı olabildiğini raporlar.
- **Projeye karşılığı:** Daha az içerik okumanın bedelsiz olmadığını ve kalite–maliyet ilişkisinin birlikte ölçülmesi gerektiğini gösteren karşı kanıttır.
- **Sınır:** Üretim sistemi karşılaştırmasıdır; buradaki tasarruf oranları dosya bulma aracına taşınamaz.
- **İnceleme:** Hakemli yayın kaydı, özet ve PDF’in giriş kısmı.

## Örnek sistemler ve teknik yazılar

Bu grupta teknik dokümantasyon, geliştirici yazısı ve ders kitabı bulunur; bunlar projenin deneysel başarı kanıtı değildir. Dokümantasyonda belirtilen yetenekler kaydedildi; kaynak kodu denetimi, kurulum veya uçtan uca test yapılmadı.

| Kimlik | Birincil kaynak | İncelenecek yön | Projeye aktarım sınırı |
| --- | --- | --- | --- |
| U01 | [Recoll](https://www.recoll.org/) ve [geliştiricinin anlamsal arama yazısı](https://www.recoll.org/pages/recoll-semantic.html) | Yerel belge indeksi, parçalara ayırma, embedding saklama ve CLI sorgusu. Yazı Ollama/Chroma ile deneysel entegrasyonu anlatır. | Projeye yakın öncül örnek. Türkçe–İngilizce başarısı gösterilmiş sayılmaz; geliştirici CPU maliyetini ve deneysel niteliği belirtiyor. |
| U02 | [txtai — resmî depo](https://github.com/neuml/txtai) ve [örnekler](https://neuml.github.io/txtai/examples/) | Yerel embedding veritabanı, seyrek/yoğun indeksler ve ilişkisel verinin birlikte kullanımı. | Kütüphane adayı ve örnek mimari; varsayılan modelin bu projeye uygun olduğu kabul edilmez. |
| U03 | [Khoj — resmî depo](https://github.com/khoj-ai/khoj) | Kişisel belgelerde anlamsal arama, Markdown desteği ve self-hosting. | Ürün kapsamı bu projeden geniştir. Self-hosting seçeneği, her yapılandırmanın internetsiz çalıştığını kanıtlamaz. |
| U04 | [Sentence Transformers: Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) | Aday getirme ile sorgu–belge çiftini yeniden puanlamanın ayrılması. | Yeniden sıralama ek hesaplama ister ve ilk aşamanın kaçırdığı belgeyi geri getiremez. Model dil kapsamı ayrıca kontrol edilir. |
| U05 | [SQLite FTS5](https://www.sqlite.org/fts5.html) | Kalıcı tam metin indeksi, BM25, highlight/snippet ve güncelleme işlemleri. | Unicode desteği Türkçe kök bulma değildir. FTS5 BM25 puan yönü ve MATCH sorgu anlamı deneyde doğru ele alınmalıdır. |
| U06 | [Stanford: Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/html/htmledition/irbook.html) | Ters indeks, vektör uzayı, TF–IDF ve erişim değerlendirmesinin ders kitabı temeli. | Sinirsel çok dilli erişimi tek başına karşılamaz; yöntemleri doğru kavramsallaştırmak için temel okuma. |

## Okuma sırası

1. **Problemin konumu:** K01, K15, K17 ve K18. Kişisel bilgi erişimi geçmişi, dış kaynak kullanımı ve kalite–maliyet gerilimi.
2. **Yöntem aileleri:** K02, K04, K19, K20 ve K03. Sözcüksel, yoğun, geç etkileşimli, öğrenilmiş seyrek ve birleşim yaklaşımları.
3. **Dil ve değerlendirme:** K05, K06, K11, K12, K14, K23 ve K24. Modelin dil etiketi ile gerçek diller arası görevi ayırma.
4. **Dosya ve ölçek:** K08, K09, K22; ardından U01–U05. Parçadan dosyaya geçiş, arama maliyeti ve kalıcılık.
5. **Aday havuzunu genişletme:** K07, K10, K13, K21, K25 ve K26. İlk okumalar sonrasında eksik kalan soruya göre derinleşme.

Bu sıra bir model seçimi değildir; okumaların birbirini anlamlandırması içindir.
