"""Presentation-only additions for the website-generator measurement report."""
from pathlib import Path
import json,re,statistics
R=Path(__file__).resolve().parents[1]
def website(text):
 text=text.replace('From source files<br>to 10,000 pages.','From source files <br>to 10,000 pages.')
 text=re.sub(r'<!-- timing-rig:start -->.*?<!-- timing-rig:end -->','',text,flags=re.S)
 d=json.loads((__import__('evidence_sources').data_root('content/benchmarks/data')/'website-10000.json').read_text());jobs={x['id']:x for x in d['jobs']}
 for j in d['jobs']:
  measured=[x for x in j['samples'] if not x['warmup']]
  assert len(measured)==5 and all(x['correct'] for x in j['samples'])
  assert statistics.median(x['wall_ms'] for x in measured)==j['summary']['median_ms']
 out='<!-- timing-rig:start --><div class="rig-readout"><div class="rig-meta"><span>10,000 minimal pages</span><span>Nift · Hugo · Astro · VitePress</span><span>1 logical CPU / EPYC 7601</span><span>5 samples + 1 warmup</span></div><div class="rig-modes">'
 for mode,title in [('application-cold','01 / Fresh-fixture full'),('warm-full','02 / Warm full')]:
  out+=f'<figure class="timing-panel"><figcaption>{title}</figcaption><div class="ruler"><span>BUILD START / 0</span><span>300s / BUILD END</span></div>'
  for n in ['Nift','Hugo','Astro','VitePress']:
   v=jobs[n+'/'+mode]['summary']['median_ms']/1000;value=f'{v:.3f}' if v<100 else f'{v:.1f}';out+=f'<div class="timing-lane"><span>{n}</span><div class="timing-track"><i style="width:{v/300*100:.6f}%" aria-hidden="true"></i></div><strong>{value}s</strong></div>'
  out+='</figure>'
 out+='</div><p class="rig-note">Zero-origin 0–300s lanes · medians · shared dependencies/cache prepared. Minimal-page throughput, not a real-site ranking. <a href="#method">State and fairness boundaries ↓</a></p><div class="iteration-strip"><span>03 / Nift changed input</span>'
 for mode,title in [('no-op','No-op'),('one-page','One leaf'),('shared-template','Shared template')]:
  # IDs in the original evidence are the authoritative source.
  j=next(x for x in d['jobs'] if x['id']=='Nift/incremental/'+mode);v=j['summary']['median_ms']/1000;out+=f'<span>{title}<strong>{v:.3f}s</strong></span>'
 out+='</div><p class="rig-note">Nift-only production iteration; no competitor incremental/HMR comparison. Byte equality with full recomputation is checked.</p></div><!-- timing-rig:end -->'
 from iteration_memory import inject
 return inject(text.replace('<div class="pipeline">',out+'<div class="pipeline">',1),'website-generator')
if __name__=='__main__':
 p=R/'content/benchmarks/website-generator/index.html';p.write_text(website(p.read_text()))
