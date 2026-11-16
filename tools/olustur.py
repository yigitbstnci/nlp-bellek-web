"""Kaynak Markdown anlık görüntüsünü alır, yalnız bu depoda web çıktısı üretir."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = [
    'PROJE_TANIMI.md',
    'arastirma/KAYNAKLAR.md',
    'arastirma/LITERATUR_TARAMASI.md',
    'arastirma/ILK_HAFTA.md',
    'arastirma/bellek-sistemleri/ARASTIRMA.md',
    'arastirma/model-karsilastirma/RAPOR.md',
    'arastirma/model-karsilastirma/YEREL_LLM.md',
    'arastirma/model-karsilastirma/kaynak-metadata.json',
    'arastirma/model-karsilastirma/deney/veri.json',
    'arastirma/model-karsilastirma/deney/veri.sha256',
    'arastirma/model-karsilastirma/deney/calistir.py',
    'arastirma/model-karsilastirma/deney/veri_olustur.py',
    'arastirma/model-karsilastirma/deney/requirements-lock.txt',
    *[f'arastirma/model-karsilastirma/deney/sonuclar/{key}.json' for key in (
        'minilm', 'mpnet', 'e5-small', 'e5-base', 'e5-large', 'bge-m3', 'qwen-06', 'labse')],
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(source):
    source = source.resolve()
    if source == ROOT:
        raise SystemExit('--source ana araştırma deposunu göstermeli.')
    missing = [rel for rel in SOURCE_FILES if not (source / rel).is_file()]
    if missing:
        raise SystemExit('Eksik araştırma girdileri: ' + ', '.join(missing))
    manifest = {}
    for rel in SOURCE_FILES:
        origin = (source / rel).resolve()
        if not origin.is_relative_to(source):
            raise SystemExit(f'Kaynak kapsamı dışında: {rel}')
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, target)
        manifest[rel] = digest(origin)
    (ROOT / 'kaynaklar.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return source, manifest


def verify_links():
    for page in (ROOT / 'arastirma').rglob('*.html'):
        soup = BeautifulSoup(page.read_text(), 'html.parser')
        ids = [x['id'] for x in soup.select('[id]')]
        if len(ids) != len(set(ids)):
            raise SystemExit(f'Yinelenen bölüm kimliği: {page.relative_to(ROOT)}')
        for node in soup.select('a[href],img[src]'):
            url = urlsplit(node.get('href', node.get('src', '')))
            if url.scheme or url.netloc or not url.path:
                continue
            target = (page.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file():
                raise SystemExit(f'Kırık yayın bağlantısı: {page.relative_to(ROOT)} → {url.path}')
    pages = [ROOT/'arastirma/index.html', ROOT/'arastirma/bellek-sistemleri/index.html', ROOT/'arastirma/model-karsilastirma/index.html']
    menus = []
    for page in pages:
        soup = BeautifulSoup(page.read_text(), 'html.parser')
        menus.append([x.get_text(' ', strip=True) for x in soup.select('#main-nav a')])
        if not soup.select_one('#site-header .site-home'):
            raise SystemExit(f'Ana sayfa bağlantısı eksik: {page}')
    if any(len(menu) != 8 or menu != menus[0] for menu in menus):
        raise SystemExit('Sayfalar aynı sekiz bağlantılı menüyü kullanmıyor.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='Özel ana araştırma deposunun yerel yolu (salt okunur).')
    args = parser.parse_args()
    source_manifest = snapshot(args.source) if args.source else None
    for rel in SOURCE_FILES:
        if not (ROOT / rel).is_file():
            raise SystemExit('Eksik anlık görüntü; önce --source ile araştırma dosyalarını al: ' + rel)
    md_before = {p: digest(p) for p in (ROOT/'arastirma').rglob('*.md')}
    for script in ['defter.py', 'bellek.py', 'karsilastirma.py']:
        subprocess.run([sys.executable, str(ROOT/'tools'/script)], cwd=ROOT, check=True)
    verify_links()
    if any(digest(p) != value for p, value in md_before.items()):
        raise SystemExit('Üretim araştırma Markdown dosyalarını değiştirdi.')
    if source_manifest:
        source, manifest = source_manifest
        if any(digest(source / rel) != value for rel, value in manifest.items()):
            raise SystemExit('Ana araştırma girdisi üretim sırasında değişti; yayınlama.')
    print('Üç sayfa üretildi; bağlantılar ve ortak menü doğrulandı. Araştırma girdileri değiştirilmedi.')


if __name__ == '__main__':
    main()
