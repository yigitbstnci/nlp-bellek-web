# NLP Araştırma Defteri — web yayını

**Canlı site:** https://yigitbstnci.github.io/nlp-bellek-web/

Bu depo web şablonlarını, ortak menüyü, sayfa üreticilerini, HTML sayfalarını,
üretilmiş grafikleri ve önizlemeleri içerir. Ana araştırma deposu gizli kalır;
onun uygulama kodu, kişisel ilerleme kayıtları ve Git geçmişi buraya aktarılmaz.

## Kaynaklar nerede düzenlenir?

Araştırmanın asıl Markdown dosyaları ana depodadır. Buradaki `arastirma/` Markdown
ve deney dosyaları, yayın için alınmış sınırlı bir anlık görüntüdür. Kaynak metin
değişikliklerini ana depoda yapıp yeniden aktar; buradaki kopyaları ayrı bir
araştırma kaynağı gibi sürdürme. `kaynaklar.json`, aktarılan girdilerin SHA-256
özetlerini kaydeder; özel depo yolu veya erişim bilgisi içermez.

## Ana depodan güncelle ve üret

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 tools/olustur.py --source "/ana/arastirma/deposunun/yolu"
```

Komut yalnız açıkça listelenen araştırma Markdownlarını ve yayın eklerini okur.
Ana depoda hiçbir dosyayı değiştirmez. Üç HTML sayfası ve grafikler bu web
deposunda üretilir; yerel bağlantılar ve ortak menü kontrol edilir.

Girdi güncellemeden, yalnız bu depodaki anlık görüntüyle yeniden üretmek için:

```sh
python3 tools/olustur.py
```

Bu ikinci komut ana depoya erişim gerektirmez. Model sayfasının metni doğrudan
`arastirma/model-karsilastirma/RAPOR.md` dosyasından okunur; araştırma raporu web
üretimi sırasında yeniden yazılmaz. Etkileşimli paneller kayıtlı pilot verilerini
kullanır; tarayıcıda model çalıştırılmaz.

## Dosya düzeni

- `templates/`: üç sayfanın HTML şablonları.
- `tools/`: Markdown aktarımı, HTML/grafik üretimi ve ortak gezinme.
- `arastirma/`: yayın girdilerinin anlık görüntüsü, sayfalar ve araştırma ekleri.
- `onizlemeler/`: önceki sayfa önizlemeleri.
- `index.html`: araştırma defterine giriş yönlendirmesi.

## Yayın

Değişiklikleri gözden geçirip bu depoya commit ve push yap. GitHub Pages,
`main` dalının kökünü otomatik yayınlar. Ana araştırma deposunun dallarını veya
Git geçmişini bu depoya gönderme. Yalnız burada üretilen dosyaları yayınla.
