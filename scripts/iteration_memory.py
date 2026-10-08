"""Publish exact-workload iteration RSS without changing accepted timing tables."""
from pathlib import Path
import json,statistics,hashlib,html,re,shutil
R=Path(__file__).resolve().parents[1];BASE=R.parent/'nift-experiments';D=R/'content/data/incremental-memory'
def read(p):return json.loads(p.read_text())
def median(v):return statistics.median(v)
def distribution(v,method='median'):
 return {'samples':len(v),'statistic':method,'value_mib':max(v) if method=='maximum' else median(v),'range_mib':[min(v),max(v)],'raw_mib':v}
def cell(d):
 return f'<strong>{d["value_mib"]:,.1f}</strong><small>{d["range_mib"][0]:,.1f}–{d["range_mib"][1]:,.1f}</small>' if d['samples']>1 else f'<strong>{d["value_mib"]:,.1f}</strong>'
def snapshot(slug,raw,rows,metric,policy,provenance):
 source=__import__('evidence_sources').sources()['files'].get('content/data/incremental-memory/'+slug+'.json')
 data={'_evidence_source':source,'report':slug,'metric':metric,'sample_policy':policy,'provenance':provenance,'rows':rows};D.mkdir(parents=True,exist_ok=True);p=D/(slug+'.json');p.write_text(json.dumps(data,separators=(',',':'))+'\n');return data

def prepare_existing():
 # Capgo preserves its published maximum-across-three statistic, not a median.
 f=read(BASE/'capgo/evidence/final-benchmarks/summary.json');a=read(BASE/'capgo-agent/evidence/final-benchmarks/samples.json');rows=[]
 for title,fc,ac in [('No-op','no-op','noop'),('Docs edit','incremental-docs','docs'),('Rich docs edit','incremental-rich-mdx','rich'),('Product / marketing edit','incremental-marketing','marketing'),('Blog edit','incremental-blog-listing','blog')]:
  fv=[x['peakRssKiB']/1024 for x in f['runs'] if x['class']==fc];av=[x['peakRssKiB']/1024 for x in a if x['case']==ac];assert len(fv)==len(av)==3
  rows.append({'case':title,'Faithful Nift':distribution(fv,'maximum'),'Agent Nift':distribution(av,'maximum')})
 snapshot('capgo',{'faithful':f,'agent':a},rows,'GNU time maximum individual process RSS; not aggregate simultaneous memory','Maximum across three original runs; observed min–max shown. Existing targeted measurements retain this same maximum statistic.',{'faithful_methodology':read(BASE/'capgo/evidence/final-benchmarks/methodology.json'),'agent_methodology':read(BASE/'capgo-agent/evidence/final-benchmarks/methodology.json')})
 # Docker has five samples for each published changed-input case.
 raw=read(__import__('evidence_sources').data_root('content/sites/docker/data')/'changed.json');rows=[]
 for case in dict.fromkeys(x['case'] for x in raw):
  row={'case':case}
  for model,label in [('docker','Nift docker'),('docker-agent','Nift docker-agent')]:
   v=[x['peak_rss_kib']/1024 for x in raw if x['case']==case and x['project']==model];assert len(v)==5;row[label]=distribution(v)
  rows.append(row)
 hugo=read(BASE/'docker/investigation/c6/hugo-changed/runs.json');assert len(hugo)==30 and all(x['semantic_output_checked'] for x in hugo)
 for case in dict.fromkeys(x['case'] for x in hugo):
  v=[x['peak_rss_kib']/1024 for x in hugo if x['case']==case];assert len(v)==5;rows.append({'case':'Upstream Hugo / '+case,'Upstream Hugo production':distribution(v)})
 snapshot('docker',{'nift_original_changes':raw,'hugo_original_changes':hugo},rows,'GNU time maximum individual process/phase RSS; not aggregate simultaneous pipeline RSS','Five original samples per case: median [min–max], same Nift runs as accepted changed-input timings. Hugo is the retained initial production cohort, separate from optimized Nift; not dev/HMR or paired cohort evidence.',{'implementation_commits':read(__import__('evidence_sources').data_root('content/sites/docker/data')/'implementation-commits.json'),'measurement_environment':read(BASE/'docker/investigation/c6-optimized/environment.json'),'upstream':'6cf1b1c167f032e8a6629da211602300b623b20e','nift':'4.7.2'})
 raw=read(__import__('evidence_sources').data_root('content/sites/deno/data')/'d8-production-lifecycle.json');warm=read(__import__('evidence_sources').data_root('content/sites/deno/data')/'d9-final-profile-benchmark.json');rows=[]
 for case in ['unchanged']+list(dict.fromkeys(x['case'] for x in raw)):
  row={'case':case}
  for model,label in [('deno','Nift deno'),('deno-agent','Nift deno-agent')]:
   matches=[x for x in (warm if case=='unchanged' else raw) if x['model']==model and x['case']==('warm-normal-publication' if case=='unchanged' else case)];v=[x['maximum_measured_process_rss_mib'] for x in matches];assert len(v)==(5 if case=='unchanged' else 1);row[label]=distribution(v)
  rows.append(row)
 up=read(__import__('evidence_sources').data_root('content/sites/deno/data')/'d9-final-upstream-changed-input.json');rows.append({'case':'Upstream one-body production','Upstream Deno/Lume':distribution([max(x['maximum_measured_process_rss_mib'] for x in up['components'].values())])})
 snapshot('deno',{'lifecycle':raw,'unchanged':warm,'upstream_body':up},rows,'Maximum measured individual process/phase RSS; not aggregate simultaneous memory','Changed-input cases: single original observations. Unchanged: five-sample median [min–max]. Upstream: largest measured production phase, not dev/HMR.',{'nift':'4.8.0','authored_evidence_pin':'7d663e4212d8f976b8ba0b29d819b9331db24522','rendered_evidence_pin':'0b42efec8239f49214c821e32fe5f0cc8e389f15','upstream':'9e5dd8d930c8734defe1c3172986e6312353ac1c'})
 raw=read(__import__('evidence_sources').data_root('content/sites/temporal/data')/'summary.json');rows=[]
 for case in ['unchanged']+list(dict.fromkeys(x['case'] for x in raw['changes']+raw['lifecycle'])):
  row={'case':case}
  for model,label in [('temporal','Nift authored'),('temporal-agent','Nift rendered')]:
   if case=='unchanged':
    for key,suffix in [('maximum_individual_descendant_rss_mib','individual'),('sampled_descendant_rss_sum_peak_mib','sampled sum')]:
     x=raw['scenarios']['unchanged'][model][key];row[label+' / '+suffix]={'samples':5,'statistic':'median','value_mib':x['median'],'range_mib':x['range']}
   else:
    x=next(x for x in raw['changes']+raw['lifecycle'] if x['case']==case and x['project']==model)['measurement']
    for key,suffix in [('maximum_individual_descendant_rss_mib','individual'),('sampled_descendant_rss_sum_peak_mib','sampled sum')]:row[label+' / '+suffix]=distribution([x[key]])
  rows.append(row)
 for x in raw['upstream_changes']:
  m=x['measurement'];rows.append({'case':'Upstream '+x['case']+' production','Upstream / individual':distribution([m['maximum_individual_descendant_rss_mib']]),'Upstream / sampled sum':distribution([m['sampled_descendant_rss_sum_peak_mib']])})
 snapshot('temporal',raw,rows,'Maximum individual process/phase RSS and separate sampled descendant resident-page sum; these are different scopes','Changed-input: single original observations. Unchanged: five-sample median [min–max]. Sampled ~50ms sums can double-count shared pages, miss peaks and are not PSS. Explicit maintenance memory is outside publication.',{**raw['source_commits'],'nift_version':'4.9.0','nift_sha256':'790bbce6325b0eadce6d98fbb27527ccd4c43fa082b23d1ca3667e54022bc862'})
 # All ordinary corpus sizes and the separate targeted follow-up retain their own samples.
 raw=[read(__import__('evidence_sources').data_root('content/benchmarks/data')/f'website-{n}.json') for n in [100,1000,10000]];target=read(__import__('evidence_sources').data_root('content/benchmarks/data')/'targeted-builds.json');rows=[]
 for d in raw:
  for case in ['no-op','one-page','shared-template']:
   job=next(x for x in d['jobs'] if x['id']=='Nift/incremental/'+case);v=[x['peak_rss_kib']/1024 for x in job['samples'] if not x['warmup']];assert len(v)==5 and all(x['correct'] for x in job['samples']);rows.append({'case':f'{d["pages"]:,} pages / {case}','Original node / Nift':distribution(v)})
 for job in target['jobs']:
  if 'targeted-one-page' not in job['id']:continue
  v=[x['peak_rss_kib']/1024 for x in job['samples'] if not x['warmup']];assert len(v)==5 and all(x['correct'] for x in job['samples']);rows.append({'case':f'{job["pages"]:,} pages / explicit target','Follow-up node / Nift':distribution(v)})
 snapshot('website-generator',{'ordinary':raw,'targeted':target},rows,'Kernel waited-child high-water RSS; not aggregate simultaneous process-tree RSS','Five original measured samples per cell: median [min–max]. Targeted follow-up is a separate EPYC 7542 node; original is EPYC 7601. No cross-node ratio or competitor incremental/HMR comparison.',{'original_machine':raw[-1]['machine'],'target_machine':target['machine'],'nift':'4.7.2'})

def prepare_ai():
 upstream=read(__import__('evidence_sources').data_root('content/sites/ai-sdk/data')/'upstream-changed.json');normal=read(__import__('evidence_sources').data_root('content/sites/ai-sdk/data')/'samples.json');rows=[]
 for m,label in [('upstream','Upstream Next/Geistdocs'),('ai-sdk','Nift authored'),('ai-sdk-agent','Nift rendered')]:
  observations=[x for x in normal if x['project']==m and x['mode']=='unchanged-cached'];assert len(observations)==5
  rows.append({'case':label+' / unchanged','Individual':distribution([x['maximum_process_phase_rss_kib']/1024 for x in observations]),'Sampled sum':distribution([x['sampled_peak_sum_rss_bytes']/1048576 for x in observations])})
 for x in upstream:rows.append({'case':'Upstream / '+x['case'],'Individual':distribution([x['maximum_process_phase_rss_kib']/1024]),'Sampled sum':distribution([x['sampled_peak_sum_rss_bytes']/1048576])})
 supplemental=__import__('evidence_sources').data_root('investigation/incremental-memory/ai-sdk')/'samples.json';proofs=[];measurements=[]
 if supplemental.exists() and (__import__('evidence_sources').data_root('investigation/incremental-memory/ai-sdk')/'completion.json').exists():
  measurements=read(supplemental)
  for model in ['ai-sdk','ai-sdk-agent']:
   for suite in (['body','routes'] if model=='ai-sdk' else ['body','routes','coordinated']):
    f=__import__('evidence_sources').data_root('investigation/incremental-memory/ai-sdk')/''/model/suite/(model+'-'+suite+'-proof.json')
    if f.exists():
     for proof in read(f):
      if model=='ai-sdk-agent' and proof['case'] in ['historical-version','provider-reference','metadata-update-remove']:continue
      assert proof['incremental_forced_equal'];x=next(x for x in measurements if x['project']==model and x['suite']==suite and x['case']==proof['case']);assert x['exit_code']==0
      proofs.append(proof);rows.append({'case':('Nift authored' if model=='ai-sdk' else 'Nift rendered')+' / '+proof['case'],'Individual':distribution([x['maximum_process_phase_rss_kib']/1024]),'Sampled sum':distribution([x['sampled_peak_sum_rss_bytes']/1048576])})
 if (__import__('evidence_sources').data_root('investigation/incremental-memory/ai-sdk')/'completion.json').exists():assert len(proofs)==26
 snapshot('ai-sdk',{'original_unchanged':normal,'original_upstream_changes':upstream,'supplemental_migration_memory':measurements,'supplemental_forced_proofs':proofs},rows,'Individual = GNU maximum individual process/phase RSS, not aggregate simultaneous memory. Sampled sum = ~50ms live descendant resident-page sum, shared pages can be double-counted, short peaks missed; not PSS','Original unchanged: five-sample median [min–max]. Upstream changed inputs: original single observations. Migration changed inputs: supplemental single observations on the same active NUC, pinned accepted implementation/protocol; accepted timing values are retained separately, not paired as one original cohort.',{'implementation_revisions':{'ai-sdk':'7bb3b9f1713aed61291e73136ab100c2a6f5457c','ai-sdk-agent':'dd568e4ec671dd6ddde38f06f7e24836840f3cb4'},'upstream':'3ebefff610f96892c50be48cf1838c453e2349f7','nift':'4.8.0','supplemental_environment':read(__import__('evidence_sources').data_root('investigation/incremental-memory/ai-sdk')/'environment.json') if (__import__('evidence_sources').data_root('investigation/incremental-memory/ai-sdk')/'environment.json').exists() else None})

def memory_graph(slug):
 """Render linear, zero-based memory bars; never combine different metric scopes."""
 d=read(D/(slug+'.json')); selected=[]
 preferred=['body-1','body-100','1-bodies','100-bodies','shared-layout','layout','navigation','island-source','route-rename','rename','No-op','Docs edit','Rich docs edit','Product / marketing edit','Blog edit','1-page','100-pages','metadata']
 if slug=='ai-sdk':
  cases=['body-1','body-100','shared-layout','navigation-order','island-source','route-rename']
  for case in cases:
   matches=[r for r in d['rows'] if r['case'].startswith('Nift ') and r['case'].split(' / ')[-1]==case]
   if matches:selected.append({'case':case,**{r['case'].split(' / ')[0]:r['Individual'] for r in matches}})
 else:
  rows=[r for r in d['rows'] if not r['case'].startswith('Upstream') and r['case']!='unchanged']
  selected=[r for r in rows if any(k==r['case'] for k in preferred)]
  if slug=='website-generator' or not selected:selected=rows
  if slug=='docker':selected=rows
 groups={}
 for row in selected:
  keys=[k for k in row if k!='case' and not k.endswith(' / sampled sum')]
  groups.setdefault(tuple(keys),[]).append(row)
 title='Incremental peak memory' if slug in ['website-generator','cloudflare-docs'] else 'Iteration peak memory / RSS'
 out=f'<div class="iteration-memory-graphs memory-{slug}" id="iteration-memory-graph"><h3>{title}</h3><p>Memory for changed-input production publications, separate from full-build memory and elapsed time. Linear bars start at zero; exact values are shown in MiB.</p>'
 for keys,rows in groups.items():
  peak=max(r[k]['value_mib'] for r in rows for k in keys)
  axis=max(1,__import__('math').ceil(peak/10)*10)
  out+=f'<figure class="rss-lanes"><figcaption>{html.escape("Maximum individual process/phase RSS; sampled tree sums remain separate in the tables" if slug in ["ai-sdk","temporal"] else d["metric"])}</figcaption><div class="rss-axis"><span>0</span><span>{axis:,.0f} MiB</span></div>'
  for row in rows:
   out+='<div class="rss-event"><h4>'+html.escape(row['case'])+'</h4>'
   for i,k in enumerate(keys):
    v=row[k]['value_mib'];label=k.replace(' / individual','');out+=f'<div class="rss-signal rss-series-{i}"><div class="rss-label"><span>{html.escape(label)}</span><strong>{v:,.1f} MiB</strong></div><div class="rss-track" aria-hidden="true"><i style="width:{100*v/axis:.5f}%"></i></div></div>'
   out+='</div>'
  out+='</figure>'
 out+='<p class="qualification">'+html.escape(d['sample_policy'])+' Full case tables and evidence below retain the other scopes and workloads.</p></div>'
 return out

def panel(slug):
 p=D/(slug+'.json')
 if not p.exists():return ''
 d=read(p);columns=list(dict.fromkeys(k for row in d['rows'] for k in row if k!='case'));scope='individual' if slug not in ['website-generator'] else 'waited-child'
 wrapper={'docker':'table-wrap','deno':'data-block','ai-sdk':'table-wrap','temporal':'tablewrap','capgo':'table-scroll','website-generator':'table-scroll'}[slug]
 out=f'<div class="iteration-memory" id="iteration-memory"><h3>Iteration memory / peak RSS</h3><p>Incremental memory matters alongside elapsed time: a smaller affected build can leave more headroom for concurrent builds, CI jobs and agents on constrained machines. Shared changes and retained worker pools can still use substantial memory; an incremental build is not guaranteed to have a lower peak than a full build. Actual concurrency and total workflow productivity were not benchmarked.</p><p class="qualification">{html.escape(d["metric"])}. {html.escape(d["sample_policy"])}</p>'
 groups={}
 for row in d['rows']:
  keys=[k for k in row if k!='case']
  scopes=['individual','sampled sum'] if any(' / individual' in k for k in keys) else [None]
  for metric_scope in scopes:
   selected=[k for k in keys if metric_scope is None or k.endswith(' / '+metric_scope)]
   if selected:groups.setdefault(tuple(selected),[]).append(row)
 for columns,rows in groups.items():
  caption='Peak RSS in MiB'
  if columns[0].endswith(' / individual'):caption+=' · maximum individual process/phase'
  elif columns[0].endswith(' / sampled sum'):caption+=' · sampled descendant resident-page sum'
  out+=f'<div class="{wrapper}" role="region" tabindex="0" aria-label="{html.escape(caption)}"><table><caption>{caption} · accepted timings unchanged</caption><thead><tr><th scope="col">Case</th>'+''.join('<th scope="col">'+html.escape(k.split(' / individual')[0].split(' / sampled sum')[0])+'</th>' for k in columns)+'</tr></thead><tbody>'
  for row in rows:out+='<tr><th scope="row">'+html.escape(row['case'])+'</th>'+''.join('<td data-label="'+html.escape(k)+'">'+cell(row[k])+'</td>' for k in columns)+'</tr>'
  out+='</tbody></table></div>'
 if slug=='ai-sdk' and d['provenance'].get('supplemental_environment'):out+='<p class="qualification"><a href="@path(\'public/benchmarks/evidence/incremental-memory/ai-sdk-supplement.json\')">Supplemental measurements, forced/restoration gates, environment and input hashes ↗</a></p>'
 out+='<p class="qualification">Different scopes and hosts remain separate; full-build memory is not substituted for an edit. <a href="@path(\'public/benchmarks/evidence/incremental-memory/'+slug+'.json\')">Raw measurements, provenance and memory scopes ↗</a></p></div>'

 return __import__('evidence_sources').canonicalize_links(out)

def inject(text,slug):
 text=re.sub(r'<!-- iteration-memory-graph:start -->.*?<!-- iteration-memory-graph:end -->','',text,flags=re.S)
 text=re.sub(r'<!-- iteration-memory:start -->.*?<!-- iteration-memory:end -->','',text,flags=re.S)
 p=panel(slug)
 if not p:return text
 ids={'capgo':'iteration','docker':'changed-inputs','deno':'iteration','ai-sdk':'iteration','temporal':'iteration','website-generator':'results'}
 # Place before the matching section's close, keeping nested sections intact.
 start=re.search(r'<section\b[^>]*\bid="'+ids[slug]+r'"[^>]*>',text)
 if not start:
  # Docker calls its production edit section changed-input.
  start=re.search(r'<section\b[^>]*\bid="changed-input"[^>]*>',text)
 assert start,slug
 heading=re.search(r'</h2>',text[start.end():])
 if heading:
  place=start.end()+heading.end();text=text[:place]+'<!-- iteration-memory-graph:start -->'+memory_graph(slug)+'<!-- iteration-memory-graph:end -->'+text[place:]
 depth=1
 for m in re.finditer(r'<(/?)section\b[^>]*>',text[start.end():]):
  depth+=-1 if m[1] else 1
  if depth==0:
   pos=start.end()+m.start();return text[:pos]+'<!-- iteration-memory:start -->'+p+'<!-- iteration-memory:end -->'+text[pos:]
 raise AssertionError(slug)
if __name__=='__main__':
 prepare_existing();prepare_ai()
 for slug in ['capgo','docker','deno','ai-sdk','temporal','website-generator']:
  p=R/('content/benchmarks' if slug=='website-generator' else 'content/sites')/slug/'index.html';p.write_text(inject(p.read_text(),slug))
 print('Retained evidence validated and iteration RSS panels rendered.')
