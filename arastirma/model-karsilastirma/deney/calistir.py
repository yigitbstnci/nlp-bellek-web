"""Sabit revision, CPU/FP32, dört iş parçacığı ile küçük tekrarlanabilir pilot.
Kullanım: python calistir.py --models minilm e5-small e5-base
Model indirmeleri /tmp içindeki cache'e gider; kişisel notlar okunmaz.
"""
import os
os.environ.setdefault('HF_HOME','/tmp/nlp-model-study-hf')
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
os.environ.setdefault('OMP_NUM_THREADS','4')
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY','1')
from pathlib import Path
import argparse
import gc
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
import traceback
from datetime import datetime, timezone
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

ROOT=Path(__file__).resolve().parent
torch.set_num_threads(4)
torch.set_num_interop_threads(1)
DATA=json.loads((ROOT/'veri.json').read_text())
META={m['key']:m for m in json.loads((ROOT.parent/'kaynak-metadata.json').read_text())}
INSTRUCTION='Given a question about project notes, retrieve the source passage that answers the question.'

def dump(path,data):
    temp=path.with_suffix('.tmp')
    temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    temp.replace(path)

def intervals(rows,key):
    clusters=sorted(set(x['cluster'] for x in rows))
    means=np.array([np.mean([x[key] for x in rows if x['cluster']==c]) for c in clusters])
    rng=np.random.default_rng(20261113)
    draws=rng.choice(means,size=(2000,len(means)),replace=True).mean(axis=1)
    return [float(x) for x in np.quantile(draws,[.025,.975])]

def bench(key):
    meta=META[key]
    start=time.perf_counter()
    model=SentenceTransformer(meta['repo'],revision=meta['revision'],device='cpu',trust_remote_code=False)
    model.float().eval()
    load=time.perf_counter()-start
    def format_text(text,role):
        if key.startswith('e5-'): return ('passage: ' if role=='passage' else 'query: ')+text
        if key=='qwen-06' and role=='query': return f'Instruct: {INSTRUCTION}\nQuery: {text}'
        return text
    def encode(texts,role='text',batch_size=16):
        with torch.inference_mode():
            return model.encode([format_text(t,role) for t in texts],batch_size=batch_size,
                                normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)
    # Warm-up before latency samples. No hand-selected result affects labels or parameters.
    encode(['Bu bir ısınma cümlesidir.','This is a warm-up sentence.'])
    docs=DATA['documents']; queries=DATA['queries']
    start=time.perf_counter(); dv=encode([d['text'] for d in docs],'passage'); corpus_s=time.perf_counter()-start
    start=time.perf_counter(); qv=encode([q['text'] for q in queries],'query'); query_batch_s=time.perf_counter()-start
    score=qv@dv.T
    # Stable ties use id order; no labels enter ranking.
    ranked=np.argsort(-score,axis=1,kind='stable')
    outcomes=[]
    for q,order,ss in zip(queries,ranked,score):
        ids=[docs[int(i)]['id'] for i in order]
        rank=min(ids.index(i)+1 for i in q['relevant'])
        outcomes.append(dict(query_id=q['id'],cluster=q['cluster'],direction=q['direction'],rank=rank,
            hit1=float(rank==1),hit3=float(rank<=3),mrr=1/rank,ndcg5=1/np.log2(rank+1) if rank<=5 else 0,
            top5=[dict(id=docs[int(i)]['id'],score=float(ss[int(i)])) for i in order[:5]]))
    metrics={k:float(np.mean([o[k] for o in outcomes])) for k in ['hit1','hit3','mrr','ndcg5']}
    metrics['hit1_ci95_cluster_bootstrap']=intervals(outcomes,'hit1')
    metrics['directions']={d:{k:float(np.mean([o[k] for o in outcomes if o['direction']==d])) for k in ['hit1','hit3','mrr']} for d in ['tr-tr','en-en','tr-en','en-tr']}
    # Equal strings, default model tokenizer; record token lengths rather than pretending equality.
    timings=[]
    timing_texts=[q['text'] for q in queries[:12]]
    for _ in range(3):
        for text in timing_texts:
            t=time.perf_counter(); encode([text],'query',1); timings.append((time.perf_counter()-t)*1000)
    pair_times=[]
    pair_results=[]
    for _ in range(3):
        for pair in DATA['pairs']:
            t=time.perf_counter(); v=encode([pair['a'],pair['b']],'text',2); pair_times.append((time.perf_counter()-t)*1000)
    for pair in DATA['pairs']:
        v=encode([pair['a'],pair['b']],'text',2)
        pair_results.append(dict(id=pair['id'],cosine=float(v[0]@v[1])))
    batch=[q['text'] for q in queries[:32]]
    encode(batch,'query',16)
    bt=[]
    for _ in range(5):
        t=time.perf_counter(); encode(batch,'query',16); bt.append(time.perf_counter()-t)
    tokens=[]
    for role,texts in [('query',[q['text'] for q in queries]),('passage',[d['text'] for d in docs])]:
        enc=model.tokenizer([format_text(t,role) for t in texts],truncation=False,padding=False)
        lens=[len(x) for x in enc['input_ids']]
        tokens.append(dict(role=role,min=min(lens),mean=float(np.mean(lens)),max=max(lens),truncated=sum(n>model.max_seq_length for n in lens)))
    params=sum(p.numel() for p in model.parameters())
    result=dict(key=key,repo=meta['repo'],revision=meta['revision'],created_at=datetime.now(timezone.utc).isoformat(),
        dataset_sha256=hashlib.sha256((ROOT/'veri.json').read_bytes()).hexdigest(),
        environment=dict(platform=platform.platform(),chip=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip(),
            memory_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True)),python=platform.python_version(),device='cpu',dtype='float32',threads=4,
            versions={p:importlib.metadata.version(p) for p in ['torch','sentence-transformers','transformers','numpy','huggingface-hub']}),
        model=dict(parameters=params,dimension=int(dv.shape[1]),max_seq_length=int(model.max_seq_length),load_including_download_s=load,
            modules=str(model),query_instruction=INSTRUCTION if key=='qwen-06' else None),
        timing=dict(query_single_ms_raw=timings,query_single_median_ms=float(np.median(timings)),query_single_p95_ms=float(np.percentile(timings,95)),
            pair_encode_ms_raw=pair_times,pair_encode_median_ms=float(np.median(pair_times)),pair_encode_p95_ms=float(np.percentile(pair_times,95)),
            batch32_s_raw=bt,batch32_texts_per_s=32/float(np.median(bt)),corpus36_encode_s=corpus_s,query48_batch_encode_s=query_batch_s),
        tokens=tokens,metrics=metrics,queries=outcomes,pairs=pair_results)
    dump(ROOT/'sonuclar'/f'{key}.json',result)
    print(json.dumps(dict(key=key,status='done',r1=metrics['hit1'],ms=result['timing']['query_single_median_ms']),ensure_ascii=False),flush=True)
    del model,dv,qv;gc.collect()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--models',nargs='+',required=True)
    args=parser.parse_args();(ROOT/'sonuclar').mkdir(exist_ok=True)
    for key in args.models:
        print('START '+key,flush=True)
        try: bench(key)
        except Exception as e:
            dump(ROOT/'sonuclar'/f'{key}-error.json',dict(key=key,error=repr(e),traceback=traceback.format_exc()))
            print('ERROR '+key+': '+repr(e),flush=True)
