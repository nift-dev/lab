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
 return text.replace('<div class="pipeline">',practical+'<div class="pipeline">',1)
if __name__=='__main__':
 p=R/'content/benchmarks/website-generator/index.html';p.write_text(website(p.read_text()))
