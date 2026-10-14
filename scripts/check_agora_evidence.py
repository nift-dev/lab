#!/usr/bin/env python3
"""Verify the Agora draft against locally staged canonical evidence, no network."""
from pathlib import Path
import argparse,hashlib,json
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,default=R.parent/'nift-experiments/lab-evidence/sites/agora/20261015-optimized');a=p.parse_args();E=a.evidence
index=json.loads((E/'FILES.json').read_text())['files']
for name,record in index.items():
 f=E/name;assert f.stat().st_size==record['bytes'],name;assert hashlib.sha256(f.read_bytes()).hexdigest()==record['sha256'],name
summary=json.loads((R/'content/sites/agora/published.json').read_text())
canonical=json.loads((E/'published-summary.json').read_text())
assert summary['measured_commits']==canonical['measured_commits'] and summary['reviewed_commits']==canonical['reviewed_commits']
assert summary['publication_scope']==canonical['publication_scope']
for m in ['agora','agora-agent']:
 for case,row in summary['pipelines'][m].items():
  sample=json.loads((E/f'measurements/final-optimized/{m}-{case}.json').read_text());assert sample['exitCode']==0
  for displayed,raw in [('seconds','wallSeconds'),('tree_mib','sampledPeakTreeRssMiB'),('individual_mib','maxIndividualProcessRssMiB')]:assert row[displayed]==sample[raw],(m,case,displayed)
for i,name in enumerate(['upstream-global-warm-1','upstream-global-warm-2']):
 sample=json.loads((E/f'measurements/{name}.json').read_text());assert summary['baseline'][i]['seconds']==sample['wallSeconds'];assert summary['baseline'][i]['tree_mib']==sample['sampledPeakTreeRssMiB']
audit=json.loads((E/'investigation/final-optimized-independent-accounting.json').read_text());assert audit['referenceHtml']==2017
for v in audit['models'].values():assert not v['missingHtml'] and not v['missingNonHtmlNonbundle'] and not v['staticJsonSemanticDifferences'] and not v['markdownByteDifferences'] and v['llmMissingBlocks']==v['llmExtraBlocks']==0
assert audit['crossModel']['modules']==1657 and not audit['crossModel']['moduleByteDifferences']
restore=json.loads((E/'measurements/final-optimized/restoration-certification.json').read_text())
for v in restore.values():
 for case in ['warm','restoration']:
  assert not v[case]['nonHtmlChanged'] and not any(v[case]['normalizedComparison'].values())
proof=json.loads((E/'investigation/raw-source-invalidation-proof.json').read_text());assert proof['before_patch']['raw_search_stale'] and not proof['after_patch']['raw_search_stale']
print(f'PASS: {len(index)} evidence hashes, two upstream / ten Nift observations, scope/restoration and post-campaign source fix; no deployment')
