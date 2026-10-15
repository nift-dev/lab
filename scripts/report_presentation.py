"""Presentation-only additions for the website-generator measurement report."""
from pathlib import Path
import json,re,statistics
R=Path(__file__).resolve().parents[1]
def website(text):
 text=text.replace('From source files<br>to 10,000 pages.','From source files <br>to 10,000 pages.')
 text=re.sub(r'<!-- timing-rig:start -->.*?<!-- timing-rig:end -->','',text,flags=re.S)
 d=__import__('website_refresh').load('website-10000.json');jobs={x['id']:x for x in d['jobs']}
 for j in d['jobs']:
  measured=[x for x in j['samples'] if not x['warmup']]
  assert len(measured)==5 and all(x['correct'] for x in j['samples'])
  assert statistics.median(x['wall_ms'] for x in measured)==j['summary']['median_ms']
 out='<!-- timing-rig:start --><div class="rig-readout"><div class="rig-meta"><span>10,000 minimal pages</span><span>Nift · Hugo · Astro · VitePress</span><span>1 logical CPU / EPYC 7642</span><span>5 samples + 1 warmup</span></div><div class="rig-modes">'
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
 # Preserve the controlled rig alongside its unchanged official table.
 official=out.replace('timing-rig:start','official-timing-rig:start').replace('timing-rig:end','official-timing-rig:end').replace('10,000 minimal pages','Official CPU0 controlled cohort · 10,000 pages')
 data=json.loads((__import__('website_refresh').SUPPLEMENT/'ANALYSIS-v3.json').read_text())['main']
 practical='<!-- timing-rig:start --><div class="rig-readout"><div class="rig-meta"><span>Normal all-core supplement · 10,000 pages</span><span>Nift −1 · Hugo default</span><span>4 logical CPUs / EPYC 7642</span><span>5 samples + 1 warmup</span></div><div class="rig-modes">'
 for mode,title in [('fresh','01 / Fresh full · all-core'),('warm-full','02 / Warm full · all-core')]:
  practical+=f'<figure class="timing-panel"><figcaption>{title}</figcaption><div class="ruler"><span>BUILD START / 0</span><span>2s / BUILD END</span></div>'
  for name in ['Nift','Hugo']:
   value=data[name][mode]['median_ms']/1000
   practical+=f'<div class="timing-lane"><span>{name}</span><div class="timing-track"><i style="width:{value/2*100:.6f}%" aria-hidden="true"></i></div><strong>{value:.3f}s</strong></div>'
  practical+='</figure>'
 practical+='</div><p class="rig-note">Audited supplemental normal defaults: Nift build-threads=-1; Hugo GOMAXPROCS unset. Fresh ranges overlap; warm ranges are disjoint. This separate cohort does not replace the <a href="#results">official CPU0 controlled results ↓</a>. <a href="#parallel">Full all-core chart, CPU, RSS and workload audit ↓</a>.</p><div class="iteration-strip"><span>03 / Normal Nift incremental workflow</span>'
 for mode,title in [('no-op','No-op'),('one-page','One page')]:
  value=jobs['Nift/incremental/'+mode]['summary']['median_ms']/1000;practical+=f'<span>{title}<strong>{value:.3f}s</strong></span>'
 target=__import__('website_refresh').load('targeted-builds.json');value=next(j for j in target['jobs'] if j['id']=='Nift/10000/targeted-one-page')['summary']['median_ms']/1000
 practical+=f'<span>Targeted leaf<strong>{value:.3f}s</strong></span></div><p class="rig-note">Incremental and targeted figures retain their distinct CPU0 cohorts; no matched Hugo incremental result was measured. Normal publishing may use nift build; --all forces full work.</p></div><!-- timing-rig:end -->'
 marker='<h2>Official CPU0 controlled cohort.</h2>'
 assert marker in text
 text=text.replace(marker,marker+official,1)
 return text.replace('<div class="pipeline">',practical+'<div class="pipeline">',1)
if __name__=='__main__':
 p=R/'content/benchmarks/website-generator/index.html';p.write_text(website(p.read_text()))
