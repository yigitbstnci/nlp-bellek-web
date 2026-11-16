"""Üç araştırma notundan çevrimdışı okunabilen tek HTML rehberi üretir.
Çalıştırma: python3 tools/olustur.py
Gerekenler: markdown, beautifulsoup4
"""
from pathlib import Path
import html
import re
import markdown
from bs4 import BeautifulSoup
from gezinme import apply_navigation

ROOT = Path(__file__).resolve().parents[1] / 'arastirma'
SOURCES = {name: (ROOT / name).read_text() for name in (
    'KAYNAKLAR.md', 'LITERATUR_TARAMASI.md', 'ILK_HAFTA.md')}


def slug(s):
    s = s.casefold().replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def render(text):
    soup = BeautifulSoup(markdown.markdown(text, extensions=['tables', 'sane_lists']), 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href', '')
        routes = {'KAYNAKLAR.md': '#kaynaklar', 'LITERATUR_TARAMASI.md': '#literatur', 'ILK_HAFTA.md': '#ilk-hafta'}
        if href in routes:
            a['href'] = routes[href]
        elif href.startswith(('https://', 'http://')):
            a['target'] = '_blank'
            a['rel'] = 'noopener noreferrer'
    # Kaynak kimlikleri okuma notlarından ilgili karta götürür.
    for text_node in list(soup.find_all(string=re.compile(r'\b[KU]\d{2}\b'))):
        if text_node.find_parent(['a', 'code', 'script', 'style']):
            continue
        parts, start = [], 0
        for m in re.finditer(r'\b[KU]\d{2}\b', str(text_node)):
            parts.append(html.escape(str(text_node)[start:m.start()]))
            ident = m.group()
            parts.append(f'<a class="ref" href="#kaynaklar/{ident}">{ident}</a>')
            start = m.end()
        parts.append(html.escape(str(text_node)[start:]))
        text_node.replace_with(BeautifulSoup(''.join(parts), 'html.parser'))
    for table in soup.find_all('table'):
        wrap = soup.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0', 'role': 'region', 'aria-label': 'Karşılaştırma tablosu; yatay kaydırılabilir'})
        table.wrap(wrap)
    for li in soup.find_all('li'):
        if li.get_text().startswith('[x] '):
            li['class'] = ['done-item']
            first = li.contents[0]
            first.replace_with(str(first).replace('[x] ', '', 1))
    return str(soup)


def document(name, prefix):
    soup = BeautifulSoup(render(SOURCES[name]), 'html.parser')
    if soup.h1:
        soup.h1.decompose()
    toc = []
    for n, heading in enumerate(soup.find_all('h2'), 1):
        title = re.sub(r'^\d+\.\s*', '', heading.get_text())
        ident = f'{prefix}-{slug(title)}'
        heading['id'] = ident
        heading['tabindex'] = '-1'
        heading.string = title
        toc.append(f'<a href="#{prefix}/{ident}"><span>{n:02d}</span>{html.escape(title)}</a>')
    return str(soup), ''.join(toc)


SHORT = {
    'K01': 'Stuff I’ve Seen', 'K02': 'BM25 ve olasılıksal erişim', 'K03': 'Reciprocal Rank Fusion',
    'K04': 'Çok dilli cümle temsilleri', 'K05': 'Multilingual E5', 'K06': 'BGE-M3',
    'K07': 'Qwen3 Embedding', 'K08': 'PARADE', 'K09': 'Faiss', 'K10': 'BEIR',
    'K11': 'Mr. TyDi', 'K12': 'MIRACL', 'K13': 'MMTEB', 'K14': 'NeuCLIRBench',
    'K15': 'Retrieval-Augmented Generation', 'K16': 'Çok dilli RAG', 'K17': 'Lost in the Middle',
    'K18': 'RAG mi, uzun bağlam mı?', 'K19': 'ColBERT', 'K20': 'SPLADE', 'K21': 'LaBSE',
    'K22': 'HNSW', 'K23': 'TR-MTEB', 'K24': 'TR-TEB', 'K25': 'TurkColBERT', 'K26': 'RAGTurk',
}
GROUPS = {
    'Kişisel bilgi erişimi ve sözcüksel yöntemler': 'Kişisel erişim & sözcüksel arama',
    'Çok dilli temsil ve sıralama aileleri': 'Temsil & sıralama',
    'Değerlendirme ve veri kümeleri': 'Değerlendirme & veri',
    'Türkçe için doğrudan ilgili güncel çalışmalar': 'Türkçe odaklı çalışmalar',
    'Yapay zekâya kaynak sağlama ve maliyet iddiası': 'Yapay zekâ & maliyet',
}

source_md = SOURCES['KAYNAKLAR.md']
card_parts, records = [], []
for group_match in re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)', source_md, re.M | re.S):
    group_name, group_text = group_match.groups()
    if group_name not in GROUPS:
        continue
    group = GROUPS[group_name]
    for m in re.finditer(r'^### (K\d{2}) — ([^\n]+)\n(.*?)(?=^### |\Z)', group_text, re.M | re.S):
        ident, title, body = m.groups()
        contribution = re.search(r'^- \*\*Katkı:\*\* (.+)', body, re.M).group(1)
        meta = re.search(r'^\*\*(.+?)\*\*', body.strip()).group(1)
        year = re.search(r'\b(?:19|20)\d{2}\b', meta).group()
        paper_type = 'Teknik rapor / ön baskı' if ('teknik' in meta.lower() or 'erişilen kaynak arXiv' in meta or 'ilk arXiv' in meta or 'ilk ön' in meta or 'arXiv kaydında' in meta) else 'Akademik yayın'
        tags = [group]
        if ident in ('K09', 'K22'):
            tags.append('İndeksleme')
        if ident in ('K08',):
            tags.append('Uzun belge')
        if ident == 'K06':
            tags.extend(['BGE-M3', 'embedding'])
        full = render(body)
        card_parts.append(f'''<details class="source-card" id="{ident}" data-kind="academic" data-group="{html.escape(group)}" data-turkish="{'true' if ident in ('K23','K24','K25','K26') else 'false'}">
<summary><span class="source-id">{ident}</span><span class="source-summary"><span class="source-meta">{html.escape(group)} <span>·</span> {year}</span><strong>{html.escape(SHORT[ident])}</strong><span class="source-excerpt">{html.escape(contribution)}</span></span><span class="expand-icon" aria-hidden="true">+</span></summary>
<div class="source-body"><div class="full-title">{html.escape(title)}</div>{full}</div></details>''')
        records.append((ident, title, body))

tech_soup = BeautifulSoup(markdown.markdown(source_md, extensions=['tables']), 'html.parser')
tech_table = tech_soup.find('table')
for row in tech_table.tbody.find_all('tr'):
    cols = row.find_all('td')
    ident = cols[0].get_text()
    link = cols[1].find('a')
    title = link.get_text()
    contribution = cols[2].get_text()
    group = 'Sistemler & teknik kaynaklar'
    card_parts.append(f'''<details class="source-card" id="{ident}" data-kind="technical" data-group="{group}" data-turkish="false">
<summary><span class="source-id technical-id">{ident}</span><span class="source-summary"><span class="source-meta">{group}</span><strong>{html.escape(title)}</strong><span class="source-excerpt">{html.escape(contribution)}</span></span><span class="expand-icon" aria-hidden="true">+</span></summary>
<div class="source-body">{render(cols[1].decode_contents())}<dl class="tech-detail"><dt>İncelenecek yön</dt><dd>{html.escape(contribution)}</dd><dt>Projeye aktarım sınırı</dt><dd>{html.escape(cols[3].get_text())}</dd><dt>İnceleme düzeyi</dt><dd>Resmî dokümantasyon ve proje açıklaması. Kaynak kodu denetimi veya uçtan uca test yapılmadı.</dd></dl></div></details>''')

# Kaynak notlarındaki sıralamayı ve bağlantıları kayıpsız koru.
reading_md = source_md.split('## Okuma sırası\n', 1)[1]
reading_html = render(reading_md)
intro_md = source_md.split('## Kişisel', 1)[0]
intro_md = intro_md.split('\n', 1)[1]
tech_intro = source_md.split('## Örnek sistemler ve teknik yazılar\n', 1)[1].split('\n|', 1)[0]
literature, literature_toc = document('LITERATUR_TARAMASI.md', 'literatur')
week, week_toc = document('ILK_HAFTA.md', 'ilk-hafta')

# Aile kartları doğrudan araştırma notundaki karşılaştırma tablosundan gelir.
section3 = re.search(r'^## 3\..*?\n(.*?)(?=^## 4\.)', SOURCES['LITERATUR_TARAMASI.md'], re.M | re.S).group(1)
soup = BeautifulSoup(markdown.markdown(section3, extensions=['tables']), 'html.parser')
method_cards = []
method_names = ['Sözcüksel erişim', 'Çeviri tabanlı erişim', 'Çok dilli yoğun temsil', 'Öğrenilmiş seyrek temsil', 'Geç etkileşim', 'Sıra birleştirme', 'Yeniden sıralama']
method_tags = ['TF–IDF · BM25', 'Sorgu / belge çevirisi', 'E5 · BGE-M3 · Qwen3 · LaBSE', 'SPLADE · BGE-M3', 'ColBERT · TurkColBERT', 'RRF · Hibrit', 'Cross-encoder']
for i, row in enumerate(soup.table.tbody.find_all('tr')):
    c = row.find_all('td')
    method_cards.append(f'''<details class="method-card"{' open' if i == 0 else ''}>
<summary><span class="method-index">{i+1:02d}</span><span><span class="method-tag">{html.escape(method_tags[i])}</span><strong>{method_names[i]}</strong></span><span class="expand-icon" aria-hidden="true">+</span></summary>
<div class="method-body"><p class="method-original">{html.escape(c[0].get_text())}</p><div class="method-columns"><div><span class="field-label">Araştırılacak katkı</span><p>{html.escape(c[1].get_text())}</p></div><div><span class="field-label limit-label">Sınır & maliyet</span><p>{html.escape(c[2].get_text())}</p></div></div><div class="method-sources"><span>İlgili okumalar</span>{render(c[3].get_text())}</div></div></details>''')

sections = {
    'SOURCES': '\n'.join(card_parts), 'LITERATURE': literature, 'LITERATURE_TOC': literature_toc,
    'WEEK': week, 'WEEK_TOC': week_toc, 'READING_ORDER': reading_html,
    'SCOPE': render(intro_md + '\n' + tech_intro), 'METHODS': '\n'.join(method_cards),
    'GROUP_OPTIONS': ''.join(f'<option>{html.escape(g)}</option>' for g in [*GROUPS.values(), 'Sistemler & teknik kaynaklar']),
}
template = (ROOT.parent / 'templates/defter.html').read_text()
for key, value in sections.items():
    template = template.replace('{{' + key + '}}', value)
assert not re.search(r'\{\{[A-Z_]+\}\}', template), 'Doldurulmamış şablon alanı'
template = apply_navigation(template, 'genel')
(ROOT / 'index.html').write_text(template)
assert len(records) == 26, f'Kaynak aktarımı eksik: {len(records)}'
print(f'Üretildi: {ROOT / "index.html"} ({len(template.encode()):,} bayt; {len(records)} akademik, 6 teknik kaynak)')
