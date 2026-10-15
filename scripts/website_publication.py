"""Load only the newly audited, whole-machine website corpus campaign."""
from pathlib import Path
import json,statistics,os,html
E=Path(__file__).resolve().parents[2]/'nift-benchmarks/lab-evidence'
SERIES='20261015-website-allcore-publication-c14d068';BASE=E/'campaigns'/SERIES
SHA='c14d06835bca515a5281e41da0e40219c2d60ef0';CLI='7dd42dcee5ca4a6965f0823c0ae59198282da1eb77e0fcd4cae93a537870a6fb'
REV=os.environ.get('NIFT_WEBSITE_PUBLICATION_EVIDENCE_REVISION','')
def link(path,label):
 assert len(REV)==40,'Pin the accepted new campaign before rendering'
 return f'<a href="https://github.com/nift-experiments/lab-evidence/blob/{REV}/campaigns/{SERIES}/{path}">{html.escape(label)}</a>'
def load(name):
 gate=json.loads((BASE/'website-acceptance.json').read_text());assert gate['pass'] and gate['observations']==234 and gate['candidate_sha']==SHA
 d=json.loads((BASE/'official-allcore'/name).read_text());assert d['publishable'] and d['machine']['cpu_affinity']==[0,1,2,3] and d['tools']['Nift']['sha256']==CLI
 for j in d['jobs']:
  samples=j['samples'];measured=[x for x in samples if not x['warmup']]
  assert len(samples)==6 and len(measured)==5 and all(x['correct'] and not x['timeout'] and x['exit_code']==0 for x in samples)
  assert statistics.median(x['wall_ms'] for x in measured)==j['summary']['median_ms']
 return d
def environment(d,p,section,table):
 cpu=next((x.split(':',1)[1].strip() for x in d['machine']['cpuinfo'].splitlines() if x.startswith('model name')),'Recorded in raw identity')
 body=p('One fresh g6-standard-4 Linode in us-east: 4 vCPUs, 8 GiB RAM, Ubuntu 24.04; '+html.escape(cpu)+'. All timed processes can use CPUs 0–3. Nift build_threads=-1; Hugo GOMAXPROCS is unset. Astro and VitePress retain their normal pinned benchmark configuration. This is whole-machine parallel throughput, not the earlier CPU0 cohort.')
 body+=p('Nift v4.12.0, exact clean source '+SHA+', GCC 13.3 and normal native Make -O2. CLI SHA-256 '+CLI+'. The unchanged suite is frozen at a2890bc504cf7c55b77cd4fddae17403b7caf8ae; the separately recorded adapter changes worker policy only.')
 rows=[]
 for name,v in d['tools'].items():rows.append([name,next(iter(str(v.get('version','Recorded in raw identity') if isinstance(v,dict) else v).splitlines()),'Recorded in raw identity')])
 body+=table(['Tool','Recorded version'],rows,'Pinned tools on the new four-vCPU measurement host')
 body+=p('All 39 jobs passed independent checks: 195 measured samples and 39 warmups, 234 observations. Fresh/warm full, normal incremental and explicit targets retain their own state boundaries. Their raw samples are not pooled with previous campaigns.')
 body+=p(link('host/identity.json','Exact source and binary identities')+' · '+link('PLAN.json','Frozen all-core sample plan')+' · '+link('COMMAND-BOUNDARIES.json','Exact commands and cleanup boundaries')+' · '+link('website-acceptance.json','Independent acceptance gate')+'.')
 return section('Frozen environment','The same four-vCPU machine for every tool.',body,'machine')+section('Reproduce / scrutinise','Every new observation is retained.',p(link('official-allcore/website-100.json','100-page raw samples')+' · '+link('official-allcore/website-1000.json','1,000-page raw samples')+' · '+link('official-allcore/website-10000.json','10,000-page raw samples')+' · '+link('official-allcore/targeted-builds.json','Separate targeted cohort')+' · '+link('work-accounting/summary.json','Fixture/output work accounting')+'. Exact source, warmups, failed preflight attempts, host provenance and teardown receipts remain in the campaign. Historical evidence is unchanged.'),'reproduce')
def preference(p,section):
 return section('Practitioner judgement / AI-DX','Choose the workflow as well as the build time.',p('For a human-authored existing Hugo/theme estate, I would stay with Hugo when its conventions already fit. For a new human-plus-agent maintained site, an agent-primary site or a mixed procedural publishing project, I would choose Nift when its APIs and explicit tracking fit the requirements. These are qualitative choices, not measured authoring success rates or a universal platform ranking.')+p('Explicit source/output ownership, template dependencies, named targets and .f helper policy can make bounded agent edits easier to inspect. Familiarity to humans and safe agent reasoning are different questions. The measured incremental and targeted paths support practical iteration; the frozen harness checked complete routes, intended contents and full-rebuild parity. Those harness checks are not general product-native guarantees, and equivalent Hugo incremental/HMR recovery was not measured.'),'practitioner')

def prepare_memory():
 from iteration_memory import snapshot,distribution
 raw=[load(f'website-{n}.json') for n in (100,1000,10000)];target=load('targeted-builds.json');rows=[]
 for d in raw:
  for case in ('no-op','one-page','shared-template'):
   job=next(x for x in d['jobs'] if x['id']=='Nift/incremental/'+case)
   rows.append({'case':f'{d["pages"]:,} pages / {case}','Nift':distribution([x['peak_rss_kib']/1024 for x in job['samples'] if not x['warmup']])})
 for job in target['jobs']:
  if 'targeted-one-page' in job['id']:rows.append({'case':f'{job["pages"]:,} pages / explicit target','Nift':distribution([x['peak_rss_kib']/1024 for x in job['samples'] if not x['warmup']])})
 data={'report':'website-generator','rows':rows,'metric':'Kernel waited-child high-water RSS; not aggregate simultaneous process-tree RSS','sample_policy':'Five measured samples per cell: median [min–max]. All-core same-host final v4.12; explicit targets retain a separate serial cohort. No competitor incremental/HMR comparison.','provenance':{'campaign':SERIES,'nift_source':SHA,'machine':raw[-1]['machine']}}
 from iteration_memory import D
 (D/'website-generator.json').write_text(json.dumps(data,separators=(',',':'))+'\n')

def work_accounting(p,section,table):
 data=json.loads((BASE/'work-accounting/summary.json').read_text());rows=data['rows'];assert len(rows)==12 and all(x['correct'] for x in rows)
 body=p('Every tool satisfies the same route/title/heading/body contract. That does not mean equal emitted bytes or identical product features. These are separate untimed fresh builds on the same host; their counts explain the workload boundary, not a causal allocation of elapsed time.')
 body+=table(['Pages','Tool','Input files','Input bytes','Output files','Output bytes','New internal files','New internal bytes'],[[f'{x["pages"]:,}',x['engine'],f'{x["input_files"]:,}',f'{x["input_bytes"]:,}',f'{x["public_files"]:,}',f'{x["public_bytes"]:,}',f'{x["new_non_public_files"]:,}',f'{x["new_non_public_bytes"]:,}'] for x in rows],'Audited file/byte accounting; linked external dependencies are excluded from input bytes')
 body+=p('At 10,000 pages, VitePress emits 30,006 files totalling 3,018,844,091 bytes, including about 3.007 GB across its 10,001 HTML files. Nift emits 10,000 public files totalling 1,317,780 bytes and creates 10,001 internal metadata files totalling 6,584,541 bytes; Hugo emits 1,327,780 public bytes. The manifest records these substantial output-volume and bookkeeping differences. Timing ratios describe this frozen fixture, not equal byte throughput or a universal platform ranking.')
 body+=p(link('work-accounting/output-breakdown.json','Output-type breakdown')+' · '+link('work-accounting/summary.json','All twelve workload inventories')+'. Full path/size/hash manifests are retained alongside them.')
 return section('Work performed','Matching page semantics, different emitted work.',body,'work-accounting')
