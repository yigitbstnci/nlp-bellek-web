"""Üç bağımsız HTML sayfası için ortak, çevrimdışı çalışan gezinme."""
from html import escape
from bs4 import BeautifulSoup


LINKS = (
    ('genel', 'Genel bakış', 'index.html#genel'),
    ('yontemler', 'Modeller & yöntemler', 'index.html#yontemler'),
    ('literatur', 'Literatür notları', 'index.html#literatur'),
    ('kaynaklar', 'Kaynak kütüphanesi', 'index.html#kaynaklar'),
    ('ilk-hafta', 'İlk hafta', 'index.html#ilk-hafta'),
    ('bellek', 'Bellek sistemleri', 'bellek-sistemleri/index.html'),
    ('modeller', 'Model karşılaştırması', 'model-karsilastirma/index.html'),
    ('llm', 'Yerel LLM araştırması', 'model-karsilastirma/index.html#bolum-10'),
)

STYLE = """
:root{--site-sidebar-width:260px;--site-header-height:74px}
#sidebar.site-sidebar{position:fixed;inset:0 auto 0 0;z-index:40;width:var(--site-sidebar-width);padding:30px 22px 24px;background:#193b31;color:#dbe5dc;display:flex;flex-direction:column;overflow-y:auto;font:14px/1.5 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
html[data-theme=dark] #sidebar.site-sidebar{background:#11261e}
#sidebar .site-brand{display:block;color:#f0f2e8;text-decoration:none;font-size:16px;font-weight:650;line-height:1.5;margin:0 10px 30px}
#sidebar .site-brand small{display:block;font-size:10px;letter-spacing:.13em;color:#afc3b3;font-weight:400;margin-top:5px}
#sidebar .site-nav-label{margin:0 10px 12px;font-size:10px;letter-spacing:.15em;color:#afc3b3;text-transform:uppercase}
#main-nav{display:grid;gap:6px;margin:0}
#main-nav a{display:flex;align-items:baseline;gap:11px;padding:11px 10px;border:1px solid transparent;border-radius:4px;color:#dbe5dc;font-size:13px;line-height:1.5;text-decoration:none;overflow-wrap:normal}
#main-nav a .site-nav-num{flex:none;width:18px;color:#afc3b3;font-size:10px;font-variant-numeric:tabular-nums}
#main-nav a:hover{background:#ffffff0d}
#main-nav a[aria-current=page]{background:#ffffff0e;border-color:#5b7766;color:#fff}
#sidebar .site-nav-note{border-top:1px solid #365548;padding:20px 10px 0;margin:25px 0 0;color:#afc3b3;font-size:12px;line-height:1.8}
#sidebar .site-close{display:none}
body>.shell{margin-left:var(--site-sidebar-width);min-height:100vh}
#site-header{position:sticky;top:0;z-index:20;box-sizing:border-box;height:var(--site-header-height);min-height:var(--site-header-height);display:flex;align-items:center;justify-content:space-between;gap:16px;padding:0 30px;border-bottom:1px solid var(--line);background:var(--bg);font:14px/1.5 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
#site-header .site-location{display:flex;align-items:center;gap:16px;min-width:0}
#site-header .site-home{flex:none;color:var(--ink);font-size:13px;white-space:nowrap;text-decoration:none;padding:8px 0}
#site-header .site-home:hover{text-decoration:underline}
#site-header .site-section{font-size:12px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#site-header .site-tools{display:flex;align-items:center;gap:4px;flex:none}
#site-header button{box-sizing:border-box;display:grid;place-items:center;min-width:36px;width:36px;height:40px;min-height:40px;margin:0;padding:0;border:1px solid transparent;border-radius:4px;background:transparent;color:var(--ink);font-size:14px;line-height:1;cursor:pointer}
#site-header button:hover{background:var(--soft)}
#site-header .site-print{width:54px;font-size:12px}
#site-header #menu-toggle{display:none}
#backdrop.site-backdrop{display:none}
.progress,.reading-progress{top:73px;left:var(--site-sidebar-width)}
.mobile-toc{display:block;margin-top:25px;border:1px solid var(--line);padding:12px 16px;background:var(--paper);border-radius:4px;font-size:14px}
.mobile-toc summary{cursor:pointer;color:var(--ink)}
.mobile-toc nav{display:grid;gap:10px;margin-top:15px}
.mobile-toc nav a{display:flex;gap:10px;font-size:13px;line-height:1.7;text-decoration:none}
.mobile-toc nav a span{flex:none;margin:0}
@media(max-width:760px){
 body>.shell{margin-left:0}
 #sidebar.site-sidebar{width:min(290px,calc(100vw - 48px));visibility:hidden;transform:translateX(-100%);transition:transform .18s ease,visibility .18s}
 #sidebar.site-sidebar.open{visibility:visible;transform:translateX(0)}
 #sidebar .site-close{display:grid;place-items:center;align-self:flex-end;width:40px;height:40px;min-height:40px;margin:0 0 12px;padding:0;border:1px solid #5b7766;border-radius:4px;background:transparent;color:#f0f2e8;font-size:24px;line-height:1;cursor:pointer}
 #sidebar .site-brand{margin-bottom:22px}
 #backdrop.site-backdrop.show{display:block;position:fixed;inset:0;z-index:30;background:#071b12aa}
 body.site-menu-open{overflow:hidden}
 #site-header{padding:0 12px;gap:8px}
 #site-header .site-location{gap:8px}
 #site-header #menu-toggle{display:grid;font-size:22px}
 #site-header .site-section,#site-header .site-print{display:none}
 #site-header .site-home{font-size:12px}
 .progress,.reading-progress{left:0}
}
@media(prefers-reduced-motion:reduce){#sidebar.site-sidebar{transition:none}}
@media print{#sidebar.site-sidebar,#site-header,#backdrop.site-backdrop,.mobile-toc{display:none!important}body>.shell{margin-left:0}}
"""

SCRIPT = """
(()=>{'use strict';
const sidebar=document.getElementById('sidebar'),menu=document.getElementById('menu-toggle'),backdrop=document.getElementById('backdrop'),close=sidebar.querySelector('.site-close'),mobile=matchMedia('(max-width:760px)');
function setOpen(open,restore=false){
 open=mobile.matches&&open;
 sidebar.classList.toggle('open',open);sidebar.inert=mobile.matches&&!open;
 backdrop.classList.toggle('show',open);document.body.classList.toggle('site-menu-open',open);document.querySelector('.shell').inert=open;
 menu.setAttribute('aria-expanded',String(open));
 if(open){sidebar.setAttribute('role','dialog');sidebar.setAttribute('aria-modal','true');close.focus()}
 else{sidebar.removeAttribute('role');sidebar.removeAttribute('aria-modal');if(restore)menu.focus()}
}
menu.addEventListener('click',()=>setOpen(!sidebar.classList.contains('open')));
close.addEventListener('click',()=>setOpen(false,true));backdrop.addEventListener('click',()=>setOpen(false,true));
sidebar.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
document.addEventListener('keydown',e=>{
 if(!sidebar.classList.contains('open'))return;
 if(e.key==='Escape'){e.preventDefault();setOpen(false,true)}
 if(e.key==='Tab'){
  const items=[close,...sidebar.querySelectorAll('a[href]')],first=items[0],last=items.at(-1);
  if(e.shiftKey&&(document.activeElement===first||!sidebar.contains(document.activeElement))){e.preventDefault();last.focus()}
  else if(!e.shiftKey&&(document.activeElement===last||!sidebar.contains(document.activeElement))){e.preventDefault();first.focus()}
 }
});
mobile.addEventListener('change',()=>setOpen(false));setOpen(false);
function current(){
 const page=sidebar.dataset.page,hash=location.hash.slice(1);
 const key=page==='genel'?(hash.split('/')[0]||'genel'):page==='modeller'&&hash==='bolum-10'?'llm':page;
 sidebar.querySelectorAll('[data-nav-key]').forEach(a=>{if(a.dataset.navKey===key)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
}
addEventListener('hashchange',()=>{setOpen(false);current()});current();
document.querySelector('.skip')?.addEventListener('click',e=>{e.preventDefault();document.getElementById('content').focus();window.scrollTo({top:0,behavior:'instant'})});
})();
"""


def apply_navigation(document, page):
    """Üretilen sayfanın ortak menü ve üst çubuğunu ekler; içeriği korur."""
    soup = BeautifulSoup(document, 'html.parser')
    home = '#genel' if page == 'genel' else '../index.html#genel'

    def href(path):
        if page == 'genel':
            return path.removeprefix('index.html') if path.startswith('index.html#') else path
        return '../' + path

    links = ''.join(
        f'<a href="{escape(href(path))}" data-nav-key="{key}"'
        + (' aria-current="page"' if key == page else '')
        + f'><span class="site-nav-num">{i:02d}</span>{escape(label)}</a>'
        for i, (key, label, path) in enumerate(LINKS, 1)
    )
    aside = BeautifulSoup(f'''<aside id="sidebar" class="site-sidebar" aria-label="Ana gezinme" data-page="{page}">
<button class="site-close" type="button" aria-label="Gezinme menüsünü kapat">×</button>
<a class="site-brand" href="{home}">NLP Araştırma Defteri<small>ÇOK DİLLİ KAYNAK BULMA</small></a>
<div class="site-nav-label">Okuma alanı</div><nav id="main-nav" aria-label="Sayfalar">{links}</nav>
<p class="site-nav-note">BİL 4129 · Doğal Dil İşleme<br>Kaynaklı araştırma ve yöntem karşılaştırması.</p></aside>''', 'html.parser').aside
    old = soup.select_one('aside.sidebar, aside.site-sidebar')
    old.replace_with(aside)
    for old in soup.select('#backdrop, #site-navigation-style, #site-navigation-script'):
        old.decompose()
    aside.insert_after(BeautifulSoup('<div id="backdrop" class="site-backdrop" aria-hidden="true"></div>', 'html.parser').div)
    ids = ('font-down', 'font-up', 'theme-toggle', 'print-page') if page == 'genel' else ('smaller', 'larger', 'theme', 'print')
    title = {'genel': 'Genel bakış', 'bellek': 'Bellek sistemleri', 'modeller': 'Model karşılaştırması'}[page]
    header = BeautifulSoup(f'''<header id="site-header"><div class="site-location">
<button id="menu-toggle" type="button" aria-label="Gezinme menüsünü aç" aria-expanded="false" aria-controls="sidebar">☰</button>
<a class="site-home" href="{home}">← Ana sayfa</a><span id="crumb-section" class="site-section">{title}</span></div>
<div class="site-tools" aria-label="Okuma ayarları"><button id="{ids[0]}" type="button" aria-label="Yazıyı küçült">A−</button><button id="{ids[1]}" type="button" aria-label="Yazıyı büyüt">A+</button><button id="{ids[2]}" type="button" aria-label="Koyu temaya geç" aria-pressed="false">◐</button><button id="{ids[3]}" class="site-print" type="button" aria-label="Bu bölümü yazdır">Yazdır</button></div></header>''', 'html.parser').header
    soup.select_one('header.topbar, #site-header').replace_with(header)
    style = soup.new_tag('style', id='site-navigation-style')
    style.string = STYLE
    soup.head.append(style)
    script = soup.new_tag('script', id='site-navigation-script')
    script.string = SCRIPT
    soup.body.append(script)
    return str(soup)
