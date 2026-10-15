"""Compact audited runtime publication; canonical raw remains outside Labs."""
from pathlib import Path
import argparse,json,hashlib,html
R=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--evidence',type=Path,default=R.parent/'nift-benchmarks/lab-evidence');a.add_argument('--commit',required=True);args=a.parse_args();assert len(args.commit)==40
series='20261015-v4120-final-c14d068';candidate='c14d06835bca515a5281e41da0e40219c2d60ef0';E=args.evidence;campaign=E/'campaigns'/series

def load(p):return json.loads(p.read_text())
def audit(p):
 x=load(p/'ACCEPTANCE.json');assert x['pass'] and x['candidate_sha']==candidate
 base=p if (p/'SHA256SUMS.json').exists() else p.parent
 manifest=load(base/'SHA256SUMS.json');key=str((p/'summary.json').relative_to(base))
 assert hashlib.sha256((p/'summary.json').read_bytes()).hexdigest()==manifest[key], 'Frozen summary hash mismatch'
 return x

P=E/'benchmarks/concurrency'/series;accepted=audit(P);summary=load(P/'summary.json');old=load(R/'content/benchmarks/concurrency/published.json');cells=[]
for x in summary:
 row=[x['case'],x['mode'],x['engine'],x['median_ms']]
 if x['mode']=='persistent':row += [x['p95_ms'],x['min_ms'],x['max_ms'],x['cpu_ms'],x['tree_rss_mib'],x['max_child_rss_mib'],x['held_rss_mib'],x['samples']]
 cells.append(row)
meta=dict(old['meta']);meta.update(audit_pass=True,supported_cells=608,scenarios=64,measured_observations=10290,retained_warmups=1216,machine='One fresh four-vCPU / 8 GiB Ubuntu 24.04 Linode; AMD EPYC 7642; affinity 0–3.',versions='Nift 4.12.0 final candidate · Python 3.14.4 ordinary GIL · Node 24.21.0 · Bun 1.4.3 · Go 1.27.2',nift_sha=candidate,suite_sha=accepted['suite_sha'],experiment_sha=accepted['suite_sha'],evidence_sha=args.commit,source_summary_sha256=hashlib.sha256((P/'summary.json').read_bytes()).hexdigest(),series=series)
review='<section id="practitioner"><p class="eyebrow">AI-DX / qualitative judgment</p><h2>Which tool would I choose?</h2><p><strong>Human + agent:</strong> Go for standalone high fan-out/CPU concurrency; Nift for bounded orchestration already in a Nift project. <strong>Agent-primary:</strong> the same conditional choices. Explicit captures, typed handles and join/await help an agent inspect ownership, but they do not erase the measured throughput gaps or retained-runtime slowdown.</p><p>Exact output/error and worker-limit contracts were audited. Autonomous authoring success, race repair and recovery productivity were not measured. Harness JSON is not product-native structured feedback. Prefer concise helpers preserving explicit contracts over duplicated metadata; that is design judgment, not a timing result.</p><p>The three-version same-node queue control improved 69.48% versus release (37,528.314 → 11,455.302 ms), yet the official peer gap remains visible. Scheduling had a descriptive 8.70% higher median with overlapping ranges; three samples do not establish a regression. Node/Bun remain natural choices for an existing JS async application; networking capacity was not tested.</p></section>'
(R/'content/benchmarks/concurrency/published.json').write_text(json.dumps({'meta':meta,'cells':cells,'practitioner_html':review},separators=(',',':'))+'\n')
# Filesystem: all summary distributions, never observations/manifests.
P=E/'benchmarks/filesystem-automation'/series;rows=[]
for label in ['primary','filter-supplement']:
 audit(P/label)
 for x in load(P/label/'summary.json'):
  if x['boundary']=='booted':rows.append({'scenario':x['scenario'],'boundary':x['boundary'],'engine':x['engine'],'wall_ms':{'median':x['wall_ms']['median']}})
mem=load(E/'benchmarks/filesystem-automation/20261011-v4110/provenance/postexec-memory.json');assert mem['pass']
meta={'evidence_sha':args.commit,'series':series,'candidate_sha':candidate,'machine':'Fresh four-vCPU / 8 GiB Ubuntu 24.04 Linode; AMD EPYC 7542; affinity 0–3.','counts':'752 cells; 14,264 measured observations + 752 retained warmups; independent exact/reset/distribution audits passed.','summary_sha256':{label:hashlib.sha256((P/label/'summary.json').read_bytes()).hexdigest() for label in ['primary','filter-supplement']}}
D=R/'content/benchmarks/filesystem-automation';D.mkdir(exist_ok=True);(D/'published.json').write_text(json.dumps({'meta':meta,'cells':rows,'historical_memory':mem,'historical_memory_series':'20261011-v4110'},separators=(',',':'))+'\n')
print('Prepared compact audited concurrency608 and filesystem752 cells')
