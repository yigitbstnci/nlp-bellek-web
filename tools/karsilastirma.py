"""RAPOR.md ve kayıtlı deneylerden HTML sayfasını ve grafikleri üretir."""
from pathlib import Path
import copy
import html
import json
import re
import hashlib
import markdown
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from modeller import MODELS, SOURCES, prior

ROOT=Path(__file__).resolve().parents[1] / 'arastirma/model-karsilastirma'
from gezinme import apply_navigation
DATA=json.loads((ROOT/'deney/veri.json').read_text())
METADATA={x['key']:x for x in json.loads((ROOT/'kaynak-metadata.json').read_text())}
RESULTS={}
for f in (ROOT/'deney/sonuclar').glob('*.json'):
    r=json.loads(f.read_text())
    if 'metrics' in r: RESULTS[r['key']]=r
models=copy.deepcopy(MODELS)
for m in models:
    if m['key'] in RESULTS:
        m['params']=RESULTS[m['key']]['model']['parameters']
    m['prior']=prior(m)
    m['revision']=METADATA[m['key']]['revision']
lookup={m['key']:m for m in models}

def render(s): return markdown.markdown(s,extensions=['tables','fenced_code','sane_lists'])
ordered=[RESULTS[m['key']] for m in models if m['key'] in RESULTS]

# Exportable scientific figures. Every value comes from recorded results.
figdir=ROOT/'grafikler';figdir.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','svg.hashsalt':'nlp-bellek-web','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fffefa','axes.facecolor':'#fffefa','text.color':'#223c35','axes.labelcolor':'#39483f','xtick.color':'#64736a','ytick.color':'#39483f'})
figures=[]
def save(fig,name):
    fig.savefig(figdir/(name+'.svg'),bbox_inches='tight',metadata={'Date':None})
    svg=figdir/(name+'.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(figdir/(name+'.png'),dpi=180,bbox_inches='tight')
    plt.close(fig)

if ordered:
    rr=sorted(ordered,key=lambda r:r['timing']['query_single_median_ms'])
    y=np.arange(len(rr));med=[r['timing']['query_single_median_ms'] for r in rr];p95=[r['timing']['query_single_p95_ms'] for r in rr]
    fig,ax=plt.subplots(figsize=(9,5.1));ax.barh(y,med,color='#35694f',height=.57,label='Medyan (p50)');ax.scatter(p95,y,color='#b85d38',s=34,label='p95',zorder=3)
    ax.set_yticks(y,[lookup[r['key']]['name'] for r in rr]);ax.invert_yaxis();ax.set_xlabel('Sıcak tek-sorgu kodlama süresi (ms)');ax.set_title('Şekil 1 · Aynı cihazda model kodlama gecikmesi',loc='left',pad=18)
    ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);ax.legend(frameon=False,loc='lower right')
    for yy,v in zip(y,med): ax.text(v+.5,yy,f'{v:.1f}',va='center',fontsize=9)
    save(fig,'hiz')
    figures.append(('hiz','Şekil 1. Apple M3 · CPU/FP32 · 4 iş parçacığı. 36 sıcak tek-sorgu örneği; model yükleme hariç. P95 az tekrara dayanır.'))
    fig,ax=plt.subplots(figsize=(9,5.4))
    for r in ordered:
        m=lookup[r['key']];x=r['timing']['query_single_median_ms'];yy=r['metrics']['hit1']*100
        lo,hi=r['metrics']['hit1_ci95_cluster_bootstrap']
        ax.errorbar(x,yy,yerr=[[yy-lo*100],[hi*100-yy]],fmt='o',markersize=6,color='#35694f',alpha=.8,capsize=3)
        ax.annotate(m['name'],(x,yy),xytext=(5,6 if m['key'] not in ['e5-small','labse','e5-large'] else -14),textcoords='offset points',fontsize=8)
    ax.set_xscale('log');ax.set_xlabel('Tek-sorgu medyanı (ms, log ölçek; sola doğru daha hızlı)');ax.set_ylabel('Pilot Hit@1 (%)');ax.set_ylim(0,105)
    ax.set_title('Şekil 2 · Erişim kalitesi ve hız birlikte',loc='left',pad=18);ax.grid(alpha=.18)
    save(fig,'kalite-hiz')
    figures.append(('kalite-hiz','Şekil 2. 36 sentetik kaynak, 48 soru. Dikey çizgiler 24 hedef kaynak üzerinden bootstrap aralığı; gerçek dünya genelleme aralığı değildir.'))
    fig,ax=plt.subplots(figsize=(8.5,5.2));directions=['tr-tr','en-en','tr-en','en-tr']
    mat=np.array([[r['metrics']['directions'][d]['hit1']*100 for d in directions] for r in ordered])
    im=ax.imshow(mat,cmap='YlGn',vmin=0,vmax=100,aspect='auto');ax.set_yticks(range(len(ordered)),[lookup[r['key']]['name'] for r in ordered]);ax.set_xticks(range(4),['TR → TR','EN → EN','TR → EN','EN → TR'])
    for i in range(len(ordered)):
        for j in range(4): ax.text(j,i,f'{mat[i,j]:.1f}',ha='center',va='center',color='white' if mat[i,j]>75 else '#223c35')
    ax.set_title('Şekil 3 · Dil yönlerine göre ilk sırada bulma',loc='left',pad=18);fig.colorbar(im,ax=ax,label='Hit@1 (%)',shrink=.85)
    save(fig,'dil-yonleri')
    figures.append(('dil-yonleri','Şekil 3. Her sütunda 12 soru. Bir soru yaklaşık 8,3 yüzde puandır; küçük farkları kesin üstünlük olarak okumayın.'))

# Araştırma Markdown'ı kaynak kabul edilir; burada yeniden yazılmaz.
report=(ROOT/'RAPOR.md').read_text().replace('https://yigitbstnci.github.io/nlp-bellek-web/arastirma/model-karsilastirma/grafikler/','grafikler/')
soup=BeautifulSoup(render(report),'html.parser');soup.h1.decompose();toc=[]
for i,h in enumerate(soup.find_all('h2'),1):
    h['id']=f'bolum-{i}';toc.append(f'<a href="#bolum-{i}"><span>{i:02d}</span>{html.escape(re.sub(r"^\d+\.\s*","",h.get_text()))}</a>')
for i,h in enumerate(list(soup.find_all('h3')),1):
    if not re.match(r'^M\d{2} ·',h.get_text()): continue
    title=h.get_text();m=next(m for m in models if title.endswith(m['name']));key=m['key']
    nodes=[]
    for node in list(h.next_siblings):
        if node.name in ['h2','h3']: break
        nodes.append(node)
    card=soup.new_tag('details',attrs={'class':'model-card','id':'model-'+key,'data-family':m['family']})
    sm=soup.new_tag('summary');sm.append(BeautifulSoup(f'<span class="model-family">{html.escape(m["family"])}</span><strong>{html.escape(title)}</strong><span class="model-meta">{m["params"]/1e6:.0f}M · {m["dim"]} boyut · {m["tokens"]:,} token · {"yerel ölçüm var" if key in RESULTS else "belge incelemesi"}</span><span class="expand">+</span>','html.parser'))
    card.append(sm);body=soup.new_tag('div',attrs={'class':'model-body'})
    for node in nodes: body.append(node.extract())
    card.append(body);h.replace_with(card)
for table in soup.find_all('table'):
    table.wrap(soup.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':'Karşılaştırma tablosu; yatay kaydırılabilir'}))
for a in soup.find_all('a',href=True):
    if a['href'].startswith('https://'): a['target']='_blank';a['rel']='noopener noreferrer'

bundle=dict(models=models,results=RESULTS,data=DATA,generated='2026-11-14',dataset_sha256=hashlib.sha256((ROOT/'deney/veri.json').read_bytes()).hexdigest())
# Raw measurements remain in linked JSON; browser only needs aggregates.
for r in bundle['results'].values():
    r['timing']={k:v for k,v in r['timing'].items() if not k.endswith('_raw')}
jsontext=json.dumps(bundle,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
template=(ROOT.parents[1]/'templates/modeller.html').read_text()
base=(ROOT.parents[1]/'templates/bellek.html').read_text().split('<style>',1)[1].split('</style>',1)[0]
template=template.replace('{{BASE_STYLE}}',base)
output=template.replace('{{CONTENT}}',str(soup)).replace('{{TOC}}',''.join(toc)).replace('{{DATA}}',jsontext).replace('{{MEASURED}}',str(len(ordered)))
assert '{{' not in output
output = apply_navigation(output, 'modeller')
(ROOT/'index.html').write_text(output)
print(f'Üretildi: {len(models)} ana model, {len(ordered)} ölçüm, {len(figures)} grafik, {len(output.encode()):,} bayt')
