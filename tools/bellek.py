"""ARASTIRMA.md kaynağından bağımsız, çevrimdışı HTML okuma sayfası üretir."""
from pathlib import Path
import re
import html
import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1] / 'arastirma/bellek-sistemleri'
from gezinme import apply_navigation
soup = BeautifulSoup(markdown.markdown((ROOT / 'ARASTIRMA.md').read_text(), extensions=['tables', 'fenced_code']), 'html.parser')
soup.h1.decompose()
toc = []
for n, heading in enumerate(soup.find_all('h2'), 1):
    heading['id'] = f'bolum-{n}'
    title = re.sub(r'^\d+\.\s*', '', heading.get_text())
    heading.string = title
    toc.append(f'<a href="#bolum-{n}"><span>{n:02d}</span>{html.escape(title)}</a>')

families = []
for heading in list(soup.find_all('h3')):
    if not re.match(r'^\d{2} · ', heading.get_text()):
        continue
    body = []
    for node in list(heading.next_siblings):
        if node.name in ('h2', 'h3'):
            break
        body.append(node)
    title = heading.get_text()
    ident = 'sistem-' + title[:2]
    family = next(x.get_text().replace('Aile: ', '') for x in body if getattr(x, 'name', '') == 'p' and x.get_text().startswith('Aile:'))
    goal = next(x.get_text().replace('Çıkış hedefi: ', '') for x in body if getattr(x, 'name', '') == 'p' and x.get_text().startswith('Çıkış hedefi:'))
    if family not in families:
        families.append(family)
    card = soup.new_tag('details', attrs={'class': 'system', 'id': ident, 'data-family': family})
    summary = soup.new_tag('summary')
    summary.append(BeautifulSoup(f'<span class="family">{html.escape(family)}</span><strong>{html.escape(title)}</strong><span class="goal">{html.escape(goal)}</span><span class="expand" aria-hidden="true">+</span>', 'html.parser'))
    card.append(summary)
    content = soup.new_tag('div', attrs={'class': 'system-body'})
    for node in body:
        content.append(node.extract())
    card.append(content)
    heading.replace_with(card)

for link in soup.find_all('a', href=True):
    if link['href'] == '../LITERATUR_TARAMASI.md':
        link['href'] = '../index.html#literatur'
    if link['href'].startswith('https://'):
        link['target'] = '_blank'
        link['rel'] = 'noopener noreferrer'
for table in soup.find_all('table'):
    table.wrap(soup.new_tag('div', attrs={'class': 'table-wrap', 'tabindex': '0', 'role': 'region', 'aria-label': 'Karşılaştırma tablosu, yatay kaydırılabilir'}))

filters = '<option value="all">Bütün aileler</option>' + ''.join(f'<option>{html.escape(x)}</option>' for x in families)
controls = BeautifulSoup(f'''<div class="system-tools"><label>Sistemlerde ara<input id="search" type="search" placeholder="Örn. Avenox, token, grafik…"></label><label>Yaklaşım ailesi<select id="family">{filters}</select></label><button id="reset" type="button">Sıfırla</button><p id="count" role="status">12 / 12 yaklaşım</p></div><p id="empty" hidden>Bu aramada sonuç yok. Aramayı temizle veya bütün aileleri seç.</p>''', 'html.parser')
soup.select_one('.system').insert_before(controls)

template = (ROOT.parents[1] / 'templates/bellek.html').read_text()
template = template.replace('{{CONTENT}}', str(soup)).replace('{{TOC}}', ''.join(toc))
assert len(soup.select('.system')) == 12
assert '{{' not in template
template = apply_navigation(template, 'bellek')
(ROOT / 'index.html').write_text(template)
print(f'Üretildi: {ROOT / "index.html"} — 12 sistem, {len(toc)} bölüm')
