from pathlib import Path
"""Render compact, audited publication medians; raw evidence stays in lab-evidence.

Use the external benchmark plotting environment documented in README. --preview
permits local feasibility data only; normal publication requires accepted identities.
"""
import json,math,html,argparse
R=Path(__file__).resolve().parents[1]
E=['nift','python','node','bun','go'];N=['Nift v4.12 final','Python','Node','Bun','Go'];C=['#abff5b','#ffbd9a','#d2b4ef','#e9dc91','#88cdb5']
a=argparse.ArgumentParser();a.add_argument('input',nargs='?',default=str(R/'content/benchmarks/concurrency/published.json'));a.add_argument('--preview',action='store_true');args=a.parse_args();d=json.loads(Path(args.input).read_text());cells=d['cells'];meta=d['meta'];
if not args.preview:
 assert meta['audit_pass'] and len(cells)==meta['supported_cells']
 assert len(meta['evidence_sha'])==40 and len(meta['source_summary_sha256'])==64
S={(x[0],x[1],x[2]):x for x in cells}
for row in cells:
 if row[1]=='persistent':
  row.extend([S[('cpu-1','persistent',row[2])][3]/row[3] if row[0].startswith('cpu-') else None, int(row[0].split('-')[1])*1000/row[3] if row[0].startswith('queue-') else None])
UNITS={3:'median ms',8:'sampled tree RSS MiB',10:'held tree RSS MiB',12:'speedup ×',13:'messages / second'}
P=R/'content/benchmarks/concurrency';P.mkdir(parents=True,exist_ok=True);A=R/'public/benchmarks/concurrency/assets';A.mkdir(parents=True,exist_ok=True)
def label(n):
 parts=n.split('-')
 if parts[0] in ['schedule','tiny','fan']:return parts[-1]+' tasks'
 if parts[0]=='files':return parts[-1]+' files'
 if n.startswith('waiting-memory-'):return parts[-1]+' held tasks'
 if parts[0]=='cpu':return parts[-1]+' worker'+('s' if parts[-1]!='1' else '')
 if parts[0]=='queue':return parts[1]+' / '+parts[2]+'→'+parts[3]
 if parts[0]=='pool':return parts[1]+' / '+parts[2]+' workers'
 if parts[0]=='atomic':return 'atomic / '+parts[1]+' workers'
 if parts[0]=='mutex':return 'mutex / '+parts[1]+' increments / '+parts[2]+' workers'
 if n=='wait-100':return '100 × 10ms'
 if n=='wait-1000':return '1000 × 10ms'
 return n

def fmt(v):return '—' if v is None else f'{v:,.3f}'
def table(names,mode='persistent',metric=3):
 out='<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable exact results"><table><caption>'+('Booted isolated request' if mode=='persistent' else 'Fresh invocation')+' / '+UNITS[metric]+'</caption><colgroup><col class="label-col">'+''.join('<col>' for _ in E)+'</colgroup><thead><tr><th scope="col">Workload</th>'+''.join(f'<th scope="col" style="color:{c}">{n}</th>' for n,c in zip(N,C))+'</tr></thead><tbody>'
 for name in names:
  out+='<tr><th scope="row">'+label(name)+'</th>'+''.join('<td>'+fmt(S.get((name,mode,e),[None]*14)[metric])+'</td>' for e in E)+'</tr>'
 return out+'</tbody></table></div>'
def graph(key,title,names,metric=3):
 import os,tempfile,re
 os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'concurrency-matplotlib'))
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'svg.fonttype':'none','svg.hashsalt':'concurrency-c14d068-final','font.family':'DejaVu Sans Mono','font.size':10,'text.color':'#d7dfd6','axes.labelcolor':'#d7dfd6','xtick.color':'#d7dfd6','ytick.color':'#d7dfd6'})
 values=[S[(n,'persistent',e)][metric] for n in names for e in E if (n,'persistent',e) in S and S[(n,'persistent',e)][metric] is not None];lo=min(values);hi=max(values);log=hi/lo>100 if lo>0 else False
 fig,ax=plt.subplots(figsize=(9,3.3),dpi=100);fig.patch.set_facecolor('#1c211d');ax.set_facecolor('#1c211d');fig.subplots_adjust(left=.09,right=.96,bottom=.22,top=.77)
 for e,n,c in zip(E,N,C):
  ys=[S.get((case,'persistent',e),[None]*14)[metric] for case in names];ys=[float('nan') if y is None else y for y in ys];ax.plot(range(len(names)),ys,color=c,marker='o',linewidth=1.6,markersize=4)
  fig.text((366.6+E.index(e)*129.6)/900,.93,n,ha='right',color=c,fontsize=10)
 if log:
  from matplotlib.ticker import FuncFormatter,NullLocator
  ax.set_yscale('log');ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:g}'));ax.yaxis.set_minor_locator(NullLocator())
 else:ax.set_ylim(bottom=0)
 ax.set_title('Nift v4.12 final · '+title,loc='left',fontsize=10,pad=35)
 ax.set_xticks(range(len(names)),[label(n) for n in names]);ax.tick_params(axis='x',labelsize=9);ax.set_ylabel({3:'Booted isolated request (ms)',8:'Sampled tree RSS (MiB)',10:'Held tree RSS (MiB)',12:'Speedup vs one worker',13:'Messages per second'}[metric],fontsize=9);ax.grid(axis='y',color='#354034',linewidth=.7)
 for spine in ax.spines.values():spine.set_color('#354034')
 fig.text(.09,.835,'LOGARITHMIC SCALE' if log else 'LINEAR SCALE',color='#a3b3a0',fontsize=9)
 path=A/f'{key}.svg';fig.savefig(path,format='svg',metadata={'Date':None,'Creator':'Nift Labs concurrency publication'})
 fig.savefig(path.with_suffix('.png'),dpi=150,pil_kwargs={'compress_level':9})
 plt.close(fig)
 svg=path.read_text();svg=re.sub(r'<metadata>.*?</metadata>','',svg,flags=re.S);svg=re.sub(r'<!--.*?-->','',svg,flags=re.S);svg=re.sub(r'>\s+<','><',svg)
 from collections import Counter
 repeated=[v for v,n in Counter(re.findall(r'style="([^"]+)"',svg)).items() if n>1]
 css=''
 for i,v in enumerate(repeated):
  svg=svg.replace('style="'+v+'"','class="c'+str(i)+'"');css+=' .c'+str(i)+'{'+v+'}'
 svg=svg.replace('</style>','</style><style>'+css+'</style>',1)
 svg=re.sub(r'(?<![A-Za-z0-9])(-?\d+\.\d{4,})(?![A-Za-z0-9])',lambda m:f'{float(m[1]):.3f}'.rstrip('0').rstrip('.'),svg)
 path.write_text(svg)
 return f'<figure><div class="plot-scroll" tabindex="0" aria-label="Scrollable chart"><img src="@path(\'public/benchmarks/concurrency/assets/{key}.svg\')" width="900" height="330" alt="{title}"></div><figcaption>{title} '+('Logarithmic ordinate; equally spaced named workloads.' if log else 'Linear ordinate; equally spaced named workloads.')+f' <a href="@path(\'public/benchmarks/concurrency/assets/{key}.svg\')">Download SVG ↗</a></figcaption></figure>'

sections=[
('schedule','Schedule almost nothing.',['schedule-10','schedule-100','schedule-1000','schedule-10000'],'Creating, joining and collecting zero-work tasks. Request/response serialization is included; these are not engine-internal scheduler nanoseconds.'),
('tiny','A little work in every branch.',['tiny-10','tiny-100','tiny-1000','tiny-10000'],'Eight exact recurrence iterations per job. Large task sets are expensive stress cells with five samples for every participant.'),
('fan','Fan out. Collect everything.',['fan-10','fan-100','fan-1000'],'Every branch has a unique ID. The oracle checks exact values, missing work and duplicate results. This is the same flat create/join shape as tiny arithmetic, retained as a separately sampled fan-out cohort; it does not imply a different executor capability.'),
('wait','Wait together.',['wait-100','wait-1000','stagger-100','mixed-wait-100'],'Nift blocking sleeps occupy native async workers. Event loops suspend promises/tasks and Go suspends goroutines. Equivalent waits do not imply parallel computation. On this four-worker native pool, 1000 × 10ms blocking sleeps have a 2500ms work/worker lower bound; suspended timers have a 10ms critical-path floor before scheduling and result overhead.'),
('cpu','Use all four cores.',['cpu-1','cpu-2','cpu-4'],'The same 64 × 200000-iteration kernel at one, two and four workers. Python uses ordinary-GIL multiprocessing; Node/Bun use worker isolates. Pools are created inside each request.'),
('pool','Give the queue a limit.',['pool-light-1','pool-light-2','pool-light-4','pool-medium-1','pool-medium-2','pool-medium-4','pool-heavy-1','pool-heavy-2','pool-heavy-4'],'One, two or four workers dispatch a fixed 64-job set. Light, medium and heavy bodies reveal the tradeoff between pool setup and useful computation.'),
('queue','Talk to each other.',['queue-1000-1-1','queue-1000-1-4','queue-1000-4-1','queue-1000-4-4','queue-10000-1-1','queue-10000-1-4','queue-10000-4-1','queue-10000-4-4','queue-100000-1-1','queue-100000-1-4','queue-100000-4-1','queue-100000-4-4'],'Capacity 64. Go uses channels, Python queue.Queue, JS an authored cooperative promise queue. Nift uses a mutex-protected ring and 1ms empty/full backoff; this is a documented channel/condition-variable gap.'),
('sync','Share state carefully.',['atomic-1','atomic-2','atomic-4','mutex-1-1','mutex-1-2','mutex-1-4','mutex-8-1','mutex-8-2','mutex-8-4'],'Genuine shared atomics only. Python atomic cells and JS native-mutex cells are unavailable (—). Mutex critical sections contain one or eight increments; all counts are exact.'),
('process','Launch. Capture. Join.',['process-10','process-100','process-1000','process-mixed','process-one-failure','process-many-failures'],'Four concurrent argv-launched identical helpers. No shell startup. Every stdout value and expected exit status is checked, including failures.'),
('files','Read together.',['files-100','files-1000','files-10000'],'Pregenerated 128-byte files, exact byte hashes, four concurrent operations. This is cached runtime/file orchestration, not a disk benchmark.'),
('mixed','Different work, one result.',['mixed-64','nested-10','nested-100','failures'],'Mixed jobs combine arithmetic, a wait and a child process. Nested parents create four children. Failures collect all outcomes and let successful siblings finish.'),
('memory','Keep work alive.',['waiting-memory-100','waiting-memory-1000','waiting-memory-10000'],'All tasks are staged behind a gate while tree RSS is sampled. Nift 10k held tasks are outside this refreshed certified matrix. A separate final-candidate probe timed out before READY after 45 seconds, with sampled peak 4,137.840 MiB below its 6 GiB guard. This is a time-censored diagnostic, not a wall/memory chart point or proof of 8 GiB infeasibility. Queued Nift futures need not have started running. Shared pages may be double-counted; this is not unique physical memory.')]
body='<main id="main"><header class="hero"><p class="eyebrow">Concurrency / control room</p><h1>Several things.<br><em>At once.</em></h1><p class="lede">Nift · Python · Node · Bun · Go<br>Equivalent problems. Different execution models.</p><div class="lanes" aria-label="Schematic execution lanes, not a measured timeline">'+''.join(f'<div><span style="color:{c}">{n}</span><i></i><b></b><i></i><b></b><small>RUN / WAIT / JOIN</small></div>' for n,c in zip(N,C))+'</div><p class="note">Execution lanes are a schematic. Charts below contain measured results; no overall concurrency score.</p></header><div class="counts">'+''.join(f'<div><strong>{meta[k]:,}</strong><span>{label}</span></div>' for k,label in [('measured_observations','measured observations'),('supported_cells','supported cells'),('retained_warmups','retained warmups'),('scenarios','workloads')])+'</div><nav class="jump" aria-label="Report sections">'+''.join(f'<a href="#{key}">{key}</a>' for key,_,_,_ in sections)+'<a href="#practitioner">practitioner</a><a href="#method">evidence</a></nav>'
body+='<section id="models"><p class="eyebrow">Execution models</p><h2>The primitive travels with the number.</h2><div class="models">'+''.join('<article><h3>'+n+'</h3><p>'+t+'</p></article>' for n,t in [('Nift','Native threads, snapshot captures, async pool, shared atomic/mutex handles.'),('Python','asyncio waits, spawn processes for CPU, threads for files/processes; ordinary GIL build.'),('Node / Bun','Promises and timers for waits; worker_threads for CPU and SAB atomics.'),('Go','Compiled goroutines, channels, sync and atomic primitives.')])+'</div></section>'
for idx,(key,title,names,prose) in enumerate(sections,1):
 assert all(any(x[0]==name for x in cells) for name in names),(key,names)
 metric=10 if key=='memory' else 13 if key=='queue' else 3;chosen=names if len(names)<=4 else names[:4]
 if key=='pool':chosen=['pool-light-4','pool-medium-4','pool-heavy-4']
 if key=='queue':chosen=['queue-1000-4-4','queue-10000-4-4','queue-100000-4-4']
 if key=='sync':chosen=['atomic-1','atomic-2','atomic-4']
 body+=f'<section id="{key}" class="report"><p class="eyebrow">{idx:02} / {key}</p><h2>{title}</h2><p>{prose}</p>'+graph(key,title,chosen,metric)+table(chosen,metric=metric)
 if len(names)>len(chosen):body+='<details><summary>All workload variants / exact medians</summary>'+table(names,metric=metric)+'</details>'
 if key!='memory':body+='<details><summary>Fresh invocation / same workload, different boundary</summary>'+table(names,'fresh')+'</details>'
 if key=='cpu':
  body+=graph('speedup','Same fixed work / CPU speedup',names,12)+table(names,metric=12)
  body+='<p class="note">Four-worker efficiency: '+', '.join(n+' '+f"{S[('cpu-4','persistent',e)][12]/4*100:.1f}%" for e,n in zip(E,N))+'. Ratios of measured medians, without a significance claim.</p>'
 if key=='memory':
  memnames=['cpu-1','cpu-2','cpu-4'];body+=graph('worker-memory','CPU pools / unranked sampled RSS accounting',memnames,8)+table(memnames,metric=8)+'<p>Unranked raw 5ms sampled peak accounting, separate from the post-READY held-task checkpoint. Sampling can catch inherited pre-exec supervisor memory, miss brief peaks and double-count shared mappings; this chart cannot rank runtime memory efficiency. A separate noop-child control rose from 16.75 to 80.75 MiB when its parent allocated 64 MiB; no constant is subtracted.</p>'
 if key=='mixed':body+='<aside><h3>When one fails</h3><p>Nift recoverable errors reach await; repeated await re-observes the error and successful siblings finish. No public thread/future cancellation API was found in this frozen source: cooperative atomic stop tokens are explicit. Python task cancellation, JS AbortSignal and Go context cancellation passed separate probes. These are different contracts, not equal fail-fast semantics.</p></aside>'
 body+='</section>'
body+='<aside><h3>Repeated-runtime retention is a separate limitation.</h3><p>The separate final-candidate ten-request trajectory passed all exact oracles, but Nift’s 1000-task latency grew from 335.638 to 2,707.692 ms. A single trajectory does not establish a version ranking or root cause. Accepted booted-isolated numbers above open a new runtime per request and do not establish long-lived throughput.</p></aside>'
body+='<section id="tails"><p class="eyebrow">Supporting distributions</p><h2>Keep the tails visible.</h2><details><summary>Booted isolated cells: median, p95, range, CPU and memory</summary><div class="table-scroll distribution"><table><thead><tr><th>Case / boundary / runtime</th><th>Median ms</th><th>p95 ms</th><th>Min–max ms</th><th>CPU ms</th><th>Sampled tree MiB</th><th>n</th></tr></thead><tbody>'
for row in [x for x in cells if x[1]=='persistent']:body+='<tr><th>'+row[0]+' / '+row[1]+' / '+row[2]+'</th><td>'+fmt(row[3])+'</td><td>'+fmt(row[4])+'</td><td>'+fmt(row[5])+'–'+fmt(row[6])+'</td><td>'+fmt(row[7])+'</td><td>'+fmt(row[8])+'</td><td>'+str(row[11])+'</td></tr>'
body+='</tbody></table></div></details><p>p95 uses nearest rank; with five samples it equals the maximum and is descriptive. 5ms tree sampling can miss short-lived processes and double-count shared mappings. CPU ticks limit short-request precision. Held tree RSS is a separate metric. Fresh distributions, maximum-individual-process RSS and process/thread counts remain in canonical evidence.</p></section>'
body+='<section id="contracts"><p class="eyebrow">Implementation contracts</p><h2>Same problem. Visible boundaries.</h2><details><summary>Queue, sharing, cancellation and ownership</summary><div class="table-scroll decision"><table><thead><tr><th>Runtime</th><th>Queue / sharing</th><th>Cancellation / lifetime</th></tr></thead><tbody>'
for n,sharing,lifetime in [('Nift','Mutex ring + polling; snapshot ordinary captures; transferable typed atomic/mutex handles','Explicit join/await; cooperative atomic stop; no public future cancel found'),('Python','queue.Queue; threading.Lock; spawn-process CPU pool','asyncio cancel; executor context cleanup; a running process needs separate policy'),('Node / Bun','Cooperative promise queue; worker isolates; SAB atomics; no native mutex cell','AbortSignal where supported; worker termination is separate from promise rejection'),('Go','Buffered channel; sync.Mutex; atomic values','Context stop signals; WaitGroup and channel close remain explicit')]:
 body+='<tr><th>'+n+'</th><td>'+sharing+'</td><td>'+lifetime+'</td></tr>'
body+='</tbody></table></div><p>All timed failure cases collect every outcome and allow successful siblings to finish. Separate cancellation probes verify each model, not an identical fail-fast contract. Worker-limit probes validate 1/2/4 active workers; Python uses distinct worker processes. Exact commands and adapter sources are retained in the experiment.</p></details></section>'
body+=d['practitioner_html']
body+='<p><a href="@path(\'benchmarks/concurrency/series/20261011-v4110/\')">Preserved original report and analytical views ↗</a></p>'
body+='<section id="method"><p class="eyebrow">Frozen method / public evidence</p><h2>Same machine. Exact results.</h2><p>'+meta['machine']+'</p><p>Fresh: start → complete work → capture → exit. Booted isolated request: a new runtime reaches boot-ready before each observation → one request → full response. Startup and exit stay outside that timer; request state is equally isolated for every participant. This does not measure steady-state repeated-request throughput. The booted request includes IPC, serialization and worker-pool setup; it is not engine-only throughput. Final candidate c14d068; workload-sensitive 5–50 samples, two retained warmups, rotated participant order, all four CPUs, no outlier deletion. Every observation passed exact count/value/hash/exit checks and an independent audit.</p><p class="identity">'+html.escape(meta['versions'])+'<br>Nift source: '+meta['nift_sha']+'<br>Measured suite: '+meta['suite_sha']+'<br>Accepted evidence: '+meta['evidence_sha']+'</p><p><a href="https://github.com/nift-experiments/lab-evidence/tree/'+meta['evidence_sha']+'/benchmarks/concurrency/'+meta['series']+'">Raw observations, warmups, semantic traces, environment and audit ↗</a> · <a href="https://github.com/nift-experiments/concurrency/blob/'+meta['experiment_sha']+'/docs/METHOD.md">Complete boundaries and commands ↗</a> · <a href="https://github.com/nift-experiments/lab-evidence/tree/'+meta['evidence_sha']+'/campaigns/'+meta['series']+'/runtime-diagnostics/concurrency/threeway">Three-way, reuse and memory-control evidence ↗</a></p><p>Filesystem cache state was not reset. Shared cloud CPUs can vary. Five runtimes solve equivalent problems with explicit model differences; these measurements certify this suite, not universal production capacity.</p></section></main>'
(P/'index.html').write_text(body+'\n');print('Rendered concurrency report',len(body.encode()),'bytes')
